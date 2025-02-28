import { writable } from 'svelte/store';
import featureTranslations from './locales/features';

type LocaleKey = 'en' | 'es';
type TranslationDict = Record<string, any>;

const translations: Record<LocaleKey, () => Promise<{ default: TranslationDict }>> = {
  en: () => import('./locales/en.json'),
  es: () => import('./locales/es.json'),
};

// Helper function to get browser language
const getBrowserLanguage = (): LocaleKey => {
  if (typeof window !== 'undefined') {
    // Get browser language
    const browserLang = navigator.language.toLowerCase();
    // Check if it starts with any of our supported languages
    if (browserLang.startsWith('es')) {
      return 'es';
    }
    // Default to English for all other languages
    return 'en';
  }
  return 'en';
};

// Get initial locale from localStorage, browser language, or default to 'en'
const getInitialLocale = (): LocaleKey => {
  if (typeof window !== 'undefined') {
    // First check localStorage for user's previous preference
    const savedLocale = localStorage.getItem('locale');
    if (savedLocale === 'es' || savedLocale === 'en') {
      return savedLocale as LocaleKey;
    }
    // If no saved preference, use browser language
    return getBrowserLanguage();
  }
  return 'en';
};

export const locale = writable<LocaleKey>(getInitialLocale());

function createTranslationStore() {
  const { subscribe, set } = writable<TranslationDict>({});

  return {
    subscribe,

    init: async (currentLocale: string) => {
      try {
        console.log(`Loading translations for ${currentLocale}`);
        const module = await translations[currentLocale as keyof typeof translations]();
        
        // Merge main translations with feature translations
        const mainTranslations = module.default || module;
        const localeFeatureTranslations: Record<string, any> = {};
        
        // Add feature translations
        Object.keys(featureTranslations).forEach((feature: string) => {
          const typedFeatureTranslations = featureTranslations as Record<string, Record<string, any>>;
          if (typedFeatureTranslations[feature] && typedFeatureTranslations[feature][currentLocale]) {
            localeFeatureTranslations[feature] = typedFeatureTranslations[feature][currentLocale];
          }
        });
        
        // Merge translations
        const mergedTranslations = {
          ...mainTranslations,
          features: {
            ...mainTranslations.features,  // Preserve original features including title
            ...localeFeatureTranslations   // Add feature-specific translations
          }
        };
        
        set(mergedTranslations);
        
        // Save locale preference to localStorage
        if (typeof window !== 'undefined') {
          localStorage.setItem('locale', currentLocale);
        }
      } catch (error) {
        console.error(`Error loading translations for ${currentLocale}:`, error);
        // Fallback to English if there's an error
        if (currentLocale !== 'en') {
          console.log('Falling back to English translations');
          const enModule = await translations.en();
          set(enModule.default || enModule);
          if (typeof window !== 'undefined') {
            localStorage.setItem('locale', 'en');
          }
        }
      }
    },
  };
}

export const t = createTranslationStore();

locale.subscribe(($locale) => {
  t.init($locale);
});
