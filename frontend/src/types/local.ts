export type LocalPlace = {
  id: number
  title: string
  location: string
  tags: string[]
  image: string
}

export type PopularKeyword = {
  rank: number
  text: string
  change: number
}