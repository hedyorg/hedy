function cov_nf69bt18w() {
  var path = "/home/capybara/repos/hedyc/static/js/index.ts";
  var hash = "baff89d6c8f44f798ac008a84ec6ad0f4871245b";
  var global = new Function("return this")();
  var gcv = "__coverage__";
  var coverageData = {
    path: "/home/capybara/repos/hedyc/static/js/index.ts",
    statementMap: {},
    fnMap: {},
    branchMap: {},
    s: {},
    f: {},
    b: {},
    _coverageSchema: "1a1c01bbd47fc00a2c39e90264f33305004495a9",
    hash: "baff89d6c8f44f798ac008a84ec6ad0f4871245b"
  };
  var coverage = global[gcv] || (global[gcv] = {});
  if (!coverage[path] || coverage[path].hash !== hash) {
    coverage[path] = coverageData;
  }
  var actualCoverage = coverage[path];
  {
    // @ts-ignore
    cov_nf69bt18w = function () {
      return actualCoverage;
    };
  }
  return actualCoverage;
}
cov_nf69bt18w();
/**
 * Entry file for the JavaScript webapp
 *
 * Functions exported from modules exported here (read that twice ;)
 * will be available in the browser as `hedyApp.myFunction(...)`.
 *
 * Files that aren't called directly from the HTML do not need to be here.
 */
export * from './modal';
export * from './app';
export * from './auth';
export * from './statistics';
export * from './logs';
export * from './tutorials/tutorial';
export * from './quiz';
export * from './teachers';
export * from './state';
export * from './initialize';
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJjb3ZfbmY2OWJ0MTh3IiwiYWN0dWFsQ292ZXJhZ2UiXSwic291cmNlcyI6WyJpbmRleC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKipcbiAqIEVudHJ5IGZpbGUgZm9yIHRoZSBKYXZhU2NyaXB0IHdlYmFwcFxuICpcbiAqIEZ1bmN0aW9ucyBleHBvcnRlZCBmcm9tIG1vZHVsZXMgZXhwb3J0ZWQgaGVyZSAocmVhZCB0aGF0IHR3aWNlIDspXG4gKiB3aWxsIGJlIGF2YWlsYWJsZSBpbiB0aGUgYnJvd3NlciBhcyBgaGVkeUFwcC5teUZ1bmN0aW9uKC4uLilgLlxuICpcbiAqIEZpbGVzIHRoYXQgYXJlbid0IGNhbGxlZCBkaXJlY3RseSBmcm9tIHRoZSBIVE1MIGRvIG5vdCBuZWVkIHRvIGJlIGhlcmUuXG4gKi9cbmV4cG9ydCAqIGZyb20gJy4vbW9kYWwnO1xuZXhwb3J0ICogZnJvbSAnLi9hcHAnO1xuZXhwb3J0ICogZnJvbSAnLi9hdXRoJztcbmV4cG9ydCAqIGZyb20gJy4vc3RhdGlzdGljcyc7XG5leHBvcnQgKiBmcm9tICcuL2xvZ3MnO1xuZXhwb3J0ICogZnJvbSAnLi90dXRvcmlhbHMvdHV0b3JpYWwnO1xuZXhwb3J0ICogZnJvbSAnLi9xdWl6JztcbmV4cG9ydCAqIGZyb20gJy4vdGVhY2hlcnMnO1xuZXhwb3J0ICogZnJvbSAnLi9zdGF0ZSc7XG5leHBvcnQgKiBmcm9tICcuL2luaXRpYWxpemUnO1xuIl0sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0lBZVk7SUFBQUEsYUFBQSxZQUFBQSxDQUFBO01BQUEsT0FBQUMsY0FBQTtJQUFBO0VBQUE7RUFBQSxPQUFBQSxjQUFBO0FBQUE7QUFBQUQsYUFBQTtBQWZaO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxjQUFjLFNBQVM7QUFDdkIsY0FBYyxPQUFPO0FBQ3JCLGNBQWMsUUFBUTtBQUN0QixjQUFjLGNBQWM7QUFDNUIsY0FBYyxRQUFRO0FBQ3RCLGNBQWMsc0JBQXNCO0FBQ3BDLGNBQWMsUUFBUTtBQUN0QixjQUFjLFlBQVk7QUFDMUIsY0FBYyxTQUFTO0FBQ3ZCLGNBQWMsY0FBYyJ9