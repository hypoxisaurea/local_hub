import { createI18n } from 'vue-i18n'
import ko from './locales/ko.json'
import en from './locales/en.json'

const messages = {
  ko,
  en,
}

export const i18n = createI18n({
  legacy: false,
  locale: typeof window !== 'undefined' ? (localStorage.getItem('localhub-locale') || 'ko') : 'ko',
  fallbackLocale: 'ko',
  messages
})

export const setLocale = (lang: 'ko' | 'en') => {
  i18n.global.locale.value = lang
  if (typeof window !== 'undefined') {
    localStorage.setItem('localhub-locale', lang)
  }
}
