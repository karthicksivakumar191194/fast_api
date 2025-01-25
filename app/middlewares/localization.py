from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from babel.support import Translations
import os


class DynamicLocalizationMiddleware(BaseHTTPMiddleware):
    """
    Dynamic Loading
    """
    def __init__(self, app: FastAPI, default_language: str = "en", supported_languages=None):
        super().__init__(app)
        self.default_language = default_language
        self.supported_languages = supported_languages or ["en", "es"]
        self.locales_dir = os.path.join(os.getcwd(), "locales")

    def detect_language(self, request: Request) -> str:
        # Check for language in query params or headers
        lang = request.query_params.get("lang")
        if lang and lang in self.supported_languages:
            return lang

        accept_language = request.headers.get("accept-language", "")
        if accept_language:
            for lang in accept_language.split(","):
                lang_code = lang.split(";")[0].strip()
                if lang_code in self.supported_languages:
                    return lang_code

        return self.default_language

    def load_translations(self, language: str, module: str) -> Translations:
        # Load the .mo file for the specific module and language
        locale_path = os.path.join(self.locales_dir, language, module, "LC_MESSAGES", "messages.mo")
        if os.path.exists(locale_path):
            return Translations.load(dirname=os.path.join(self.locales_dir, language, module))
        else:
            # Fallback to default language
            return Translations.load(dirname=os.path.join(self.locales_dir, self.default_language, module))

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        # Detect language
        language = self.detect_language(request)

        # Attach a translation loader for the request
        def get_translations(module: str) -> Translations:
            return self.load_translations(language, module)

        request.state.language = language
        request.state.get_translations = get_translations

        # Continue processing the request
        response = await call_next(request)
        return response


class MultiModuleLocalizationMiddleware(BaseHTTPMiddleware):
    """
    Preloaded Loading
    """
    def __init__(self, app: FastAPI, default_language: str = "en", supported_languages=None):
        super().__init__(app)
        self.default_language = default_language
        self.supported_languages = supported_languages or ["en", "es"]
        self.locales_dir = os.path.join(os.getcwd(), "locales")
        self.translation_cache = self.preload_all_translations()

    def preload_all_translations(self):
        # Preload translations for all languages and modules
        translation_cache = {}
        for language in self.supported_languages:
            translation_cache[language] = {}
            language_dir = os.path.join(self.locales_dir, language)
            if os.path.exists(language_dir):
                for module in os.listdir(language_dir):
                    module_path = os.path.join(language_dir, module, "LC_MESSAGES", "messages.mo")
                    if os.path.exists(module_path):
                        translation_cache[language][module] = Translations.load(
                            dirname=os.path.join(self.locales_dir, language, module)
                        )
        return translation_cache

    def detect_language(self, request: Request) -> str:
        # Detect language from query or headers
        lang = request.query_params.get("lang")
        if lang and lang in self.supported_languages:
            return lang
        accept_language = request.headers.get("accept-language", "")
        if accept_language:
            for lang in accept_language.split(","):
                lang_code = lang.split(";")[0].strip()
                if lang_code in self.supported_languages:
                    return lang_code
        return self.default_language

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        # Detect the language
        language = self.detect_language(request)

        # Attach the cached translations loader to request state
        def get_translations(module: str) -> Translations:
            return self.translation_cache.get(language, {}).get(module,
                self.translation_cache[self.default_language].get(module))

        request.state.language = language
        request.state.get_translations = get_translations

        # Proceed with the request
        response = await call_next(request)
        return response
