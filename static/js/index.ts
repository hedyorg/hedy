/**
 * Entry file for the JavaScript webapp
 *
 * Functions exported from modules exported here (read that twice ;)
 * will be available in the browser as `hedyApp.myFunction(...)`.
 *
 * Files that aren't called directly from the HTML do not need to be here.
 */
import './htmx-integration';
export * from './modal';
export * from './app';
export * from './auth';
export * from './statistics';
export * from './logs';
export * from './tutorials/tutorial';
export * from './teachers';
export * from './browser-helpers/unsaved-changes';
export * from './initialize';
export * from './debugging';