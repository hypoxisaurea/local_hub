import type { RouteLocationNormalizedLoaded } from 'vue-router'

type Locale = 'ko' | 'en'

interface SeoText {
  title: string
  description: string
}

const SITE_NAME = 'Local Hub'
const DEFAULT_IMAGE = '/banners/banner.png'

const siteUrl = () => {
  const configuredUrl = import.meta.env.VITE_PUBLIC_SITE_URL?.replace(/\/$/, '')

  if (configuredUrl) {
    return configuredUrl
  }

  return typeof window !== 'undefined' ? window.location.origin : ''
}

const absoluteUrl = (path: string) => {
  if (/^https?:\/\//i.test(path)) {
    return path
  }

  const baseUrl = siteUrl()
  if (!baseUrl) {
    return path
  }

  return new URL(path, `${baseUrl}/`).toString()
}

const setMeta = (selector: string, attribute: 'content' | 'href', value: string) => {
  let element = document.querySelector(selector) as HTMLMetaElement | HTMLLinkElement | null

  if (!element) {
    element = selector.startsWith('link')
      ? document.createElement('link')
      : document.createElement('meta')

    if (selector.includes('property=')) {
      element.setAttribute('property', selector.match(/property="([^"]+)"/)?.[1] ?? '')
    } else if (selector.includes('name=')) {
      element.setAttribute('name', selector.match(/name="([^"]+)"/)?.[1] ?? '')
    } else if (selector.includes('rel=')) {
      element.setAttribute('rel', selector.match(/rel="([^"]+)"/)?.[1] ?? '')
    }

    document.head.appendChild(element)
  }

  element.setAttribute(attribute, value)
}

const routeSeoText = (route: RouteLocationNormalizedLoaded, locale: Locale): SeoText => {
  const page = route.meta?.seo as Partial<Record<Locale, SeoText>> | undefined
  const fallback: Record<Locale, SeoText> = {
    ko: {
      title: 'Local Hub - 서울 로컬 정보 공유 커뮤니티',
      description: '서울 여행자들이 로컬 정보, 숨은 명소, 맛집, 여행 후기를 함께 공유하는 커뮤니티입니다.',
    },
    en: {
      title: 'Local Hub - Seoul Local Travel Community',
      description: 'A community where Seoul travelers share local tips, hidden gems, restaurants, and travel reviews.',
    },
  }

  return page?.[locale] ?? fallback[locale]
}

export const getShareUrl = (path?: string) => {
  const targetPath = path ?? (typeof window !== 'undefined' ? window.location.pathname + window.location.search : '/')

  return absoluteUrl(targetPath)
}

export const updateSeo = (route: RouteLocationNormalizedLoaded, locale: Locale) => {
  const { title, description } = routeSeoText(route, locale)
  const url = getShareUrl(route.fullPath)
  const image = absoluteUrl(String(route.meta?.shareImage ?? DEFAULT_IMAGE))

  document.documentElement.lang = locale
  document.title = title

  setMeta('meta[name="description"]', 'content', description)
  setMeta('link[rel="canonical"]', 'href', url)
  setMeta('meta[property="og:site_name"]', 'content', SITE_NAME)
  setMeta('meta[property="og:title"]', 'content', title)
  setMeta('meta[property="og:description"]', 'content', description)
  setMeta('meta[property="og:url"]', 'content', url)
  setMeta('meta[property="og:image"]', 'content', image)
  setMeta('meta[property="og:image:alt"]', 'content', `${SITE_NAME} preview`)
  setMeta('meta[property="og:locale"]', 'content', locale === 'ko' ? 'ko_KR' : 'en_US')
  setMeta('meta[name="twitter:title"]', 'content', title)
  setMeta('meta[name="twitter:description"]', 'content', description)
  setMeta('meta[name="twitter:image"]', 'content', image)
}

export const getShareText = (route: RouteLocationNormalizedLoaded, locale: Locale) => routeSeoText(route, locale)
