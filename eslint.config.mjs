import globals from "globals";
import pluginJs from "@eslint/js";
import eslintConfigPrettier from "eslint-config-prettier";


export default [
  pluginJs.configs.recommended,
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.jest,
        ...globals.jquery,
        bootstrap: "readonly",
        FullCalendar: "readonly",
        Cookies: "readonly",
        Chart: "readonly",
      }
    },
    rules: {
      "no-duplicate-imports": "warn",
      "camelcase": "error",
      "eqeqeq": "error",
      "dot-notation": "warn",
      "no-else-return": "warn",
      "no-var": "warn"
    },
  },
  eslintConfigPrettier,
  {
    ignores: [
      "env/*"
    ]
  }
];