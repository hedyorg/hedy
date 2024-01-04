/**
 * Initialization for ES Users
 *
 * This file is a `.mts` file so that it is compiled to an ESM file (`.mjs`).
 *
 * This is necessary because otherwise the import of `tw-elements` (which is an ESM-only
 * module) will otherwise be incorrectly translated by `esbuild`.
 */
import {
  Validation,
  Select,
  initTE,
} from "tw-elements";

initTE({ Validation, Select });