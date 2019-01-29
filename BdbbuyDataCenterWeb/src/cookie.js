import Cookies from 'js-cookie'

const COOKIE_PREFIX = 'bdb_data_center_'
const expires = 7
const domain = window.location.hostname || 'localhost'
const COOKIE_OPT = {
  expires,
  domain
}
export const setCookie = (key, value, expires) => {
  Cookies.set(`${COOKIE_PREFIX}${key}`, value, COOKIE_OPT)
}

export const getOriginCookie = key => {
  const value = Cookies.get(`${key}`)
  return (value && value !== 'undefined' && value !== 'null') ? value : null
}
export const setOriginCookie = (key, value) => Cookies.set(key, value, COOKIE_OPT)
export const rmOriginCookie = (key) => Cookies.remove(`${key}`, COOKIE_OPT)

export const getCookie = (key) => {
  const value = Cookies.get(`${COOKIE_PREFIX}${key}`)
  return (value && value !== 'undefined' && value !== 'null') ? value : null
}
export const delCookie = (key) => {
  return Cookies.remove(`${COOKIE_PREFIX}${key}`, COOKIE_OPT)
}
