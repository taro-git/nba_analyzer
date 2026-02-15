/**
 * シーズンを示す文字列の形式を定義します.
 */
export type Season = string & { readonly __brand: unique symbol };
