/* eslint-disable no-undef */
module.exports = {
  plugins: [require.resolve("@trivago/prettier-plugin-sort-imports")],
  printWidth: 120,
  importOrder: ["^@/", "^[a-z]", "^[./]"],
  importOrderSeparation: true,
  importOrderSortSpecifiers: true,
  importOrderCaseInsensitive: true,
};
