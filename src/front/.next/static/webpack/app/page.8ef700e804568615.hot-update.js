"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
self["webpackHotUpdate_N_E"]("app/page",{

/***/ "(app-pages-browser)/./app/page.tsx":
/*!**********************!*\
  !*** ./app/page.tsx ***!
  \**********************/
/***/ (function(module, __webpack_exports__, __webpack_require__) {

eval(__webpack_require__.ts("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": function() { return /* binding */ ChatBot; }\n/* harmony export */ });\n/* harmony import */ var _swc_helpers_async_to_generator__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @swc/helpers/_/_async_to_generator */ \"(app-pages-browser)/./node_modules/@swc/helpers/esm/_async_to_generator.js\");\n/* harmony import */ var _swc_helpers_object_spread__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @swc/helpers/_/_object_spread */ \"(app-pages-browser)/./node_modules/@swc/helpers/esm/_object_spread.js\");\n/* harmony import */ var _swc_helpers_object_spread_props__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @swc/helpers/_/_object_spread_props */ \"(app-pages-browser)/./node_modules/@swc/helpers/esm/_object_spread_props.js\");\n/* harmony import */ var _swc_helpers_sliced_to_array__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @swc/helpers/_/_sliced_to_array */ \"(app-pages-browser)/./node_modules/@swc/helpers/esm/_sliced_to_array.js\");\n/* harmony import */ var _swc_helpers_to_consumable_array__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @swc/helpers/_/_to_consumable_array */ \"(app-pages-browser)/./node_modules/@swc/helpers/esm/_to_consumable_array.js\");\n/* harmony import */ var _swc_helpers_ts_generator__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @swc/helpers/_/_ts_generator */ \"(app-pages-browser)/./node_modules/tslib/tslib.es6.mjs\");\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-dev-runtime */ \"(app-pages-browser)/./node_modules/next/dist/compiled/react/jsx-dev-runtime.js\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ \"(app-pages-browser)/./node_modules/next/dist/compiled/react/index.js\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var _styles_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./styles.css */ \"(app-pages-browser)/./app/styles.css\");\n/* __next_internal_client_entry_do_not_use__ default auto */ \n\n\n\n\n\n\nvar _s = $RefreshSig$();\n\n // CSS 파일 import\nfunction ChatBot() {\n    var _this = this;\n    _s();\n    var _useState = (0,_swc_helpers_sliced_to_array__WEBPACK_IMPORTED_MODULE_3__._)((0,react__WEBPACK_IMPORTED_MODULE_1__.useState)([]), 2), messages = _useState[0], setMessages = _useState[1];\n    var _useState1 = (0,_swc_helpers_sliced_to_array__WEBPACK_IMPORTED_MODULE_3__._)((0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(\"\"), 2), input = _useState1[0], setInput = _useState1[1];\n    var sendMessage = function() {\n        var _ref = (0,_swc_helpers_async_to_generator__WEBPACK_IMPORTED_MODULE_4__._)(function() {\n            var userMessage, res, data;\n            return (0,_swc_helpers_ts_generator__WEBPACK_IMPORTED_MODULE_5__.__generator)(this, function(_state) {\n                switch(_state.label){\n                    case 0:\n                        if (!input.trim()) return [\n                            2\n                        ];\n                        userMessage = input.trim();\n                        setInput(\"\");\n                        // 사용자 메시지 추가\n                        setMessages(function(prev) {\n                            return (0,_swc_helpers_to_consumable_array__WEBPACK_IMPORTED_MODULE_6__._)(prev).concat([\n                                {\n                                    user: userMessage,\n                                    bot: \"\"\n                                }\n                            ]);\n                        });\n                        return [\n                            4,\n                            fetch(\"/api/chatbot\", {\n                                method: \"POST\",\n                                headers: {\n                                    \"Content-Type\": \"application/json\"\n                                },\n                                body: JSON.stringify({\n                                    message: userMessage\n                                })\n                            })\n                        ];\n                    case 1:\n                        res = _state.sent();\n                        return [\n                            4,\n                            res.json()\n                        ];\n                    case 2:\n                        data = _state.sent();\n                        // 봇 응답 추가\n                        setMessages(function(prev) {\n                            return prev.map(function(msg, idx) {\n                                return idx === prev.length - 1 ? (0,_swc_helpers_object_spread_props__WEBPACK_IMPORTED_MODULE_7__._)((0,_swc_helpers_object_spread__WEBPACK_IMPORTED_MODULE_8__._)({}, msg), {\n                                    bot: data.response\n                                }) : msg;\n                            });\n                        });\n                        return [\n                            2\n                        ];\n                }\n            });\n        });\n        return function sendMessage() {\n            return _ref.apply(this, arguments);\n        };\n    }();\n    return /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(\"div\", {\n        className: \"container\",\n        children: /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(\"div\", {\n            className: \"chat-box\",\n            children: [\n                /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(\"h1\", {\n                    style: {\n                        fontSize: \"1.25rem\",\n                        fontWeight: \"bold\",\n                        textAlign: \"center\"\n                    },\n                    children: \"ChatBot\"\n                }, void 0, false, {\n                    fileName: \"C:\\\\Users\\\\seohy\\\\Desktop\\\\boostcamp_AITech\\\\LabQ\\\\level4-nlp-finalproject-hackathon-nlp-09-lv3\\\\src\\\\front\\\\app\\\\page.tsx\",\n                    lineNumber: 38,\n                    columnNumber: 9\n                }, this),\n                /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(\"div\", {\n                    className: \"message-container\",\n                    children: messages.map(function(msg, idx) {\n                        return /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(\"div\", {\n                            style: {\n                                marginBottom: \"8px\"\n                            },\n                            children: [\n                                /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(\"p\", {\n                                    className: \"user-message\",\n                                    children: [\n                                        /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(\"strong\", {\n                                            children: \"User:\"\n                                        }, void 0, false, {\n                                            fileName: \"C:\\\\Users\\\\seohy\\\\Desktop\\\\boostcamp_AITech\\\\LabQ\\\\level4-nlp-finalproject-hackathon-nlp-09-lv3\\\\src\\\\front\\\\app\\\\page.tsx\",\n                                            lineNumber: 43,\n                                            columnNumber: 17\n                                        }, _this),\n                                        \" \",\n                                        msg.user\n                                    ]\n                                }, void 0, true, {\n                                    fileName: \"C:\\\\Users\\\\seohy\\\\Desktop\\\\boostcamp_AITech\\\\LabQ\\\\level4-nlp-finalproject-hackathon-nlp-09-lv3\\\\src\\\\front\\\\app\\\\page.tsx\",\n                                    lineNumber: 42,\n                                    columnNumber: 15\n                                }, _this),\n                                /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(\"p\", {\n                                    className: \"bot-message\",\n                                    children: [\n                                        /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(\"strong\", {\n                                            children: \"Bot:\"\n                                        }, void 0, false, {\n                                            fileName: \"C:\\\\Users\\\\seohy\\\\Desktop\\\\boostcamp_AITech\\\\LabQ\\\\level4-nlp-finalproject-hackathon-nlp-09-lv3\\\\src\\\\front\\\\app\\\\page.tsx\",\n                                            lineNumber: 46,\n                                            columnNumber: 17\n                                        }, _this),\n                                        \" \",\n                                        msg.bot || \"Typing...\"\n                                    ]\n                                }, void 0, true, {\n                                    fileName: \"C:\\\\Users\\\\seohy\\\\Desktop\\\\boostcamp_AITech\\\\LabQ\\\\level4-nlp-finalproject-hackathon-nlp-09-lv3\\\\src\\\\front\\\\app\\\\page.tsx\",\n                                    lineNumber: 45,\n                                    columnNumber: 15\n                                }, _this)\n                            ]\n                        }, idx, true, {\n                            fileName: \"C:\\\\Users\\\\seohy\\\\Desktop\\\\boostcamp_AITech\\\\LabQ\\\\level4-nlp-finalproject-hackathon-nlp-09-lv3\\\\src\\\\front\\\\app\\\\page.tsx\",\n                            lineNumber: 41,\n                            columnNumber: 13\n                        }, _this);\n                    })\n                }, void 0, false, {\n                    fileName: \"C:\\\\Users\\\\seohy\\\\Desktop\\\\boostcamp_AITech\\\\LabQ\\\\level4-nlp-finalproject-hackathon-nlp-09-lv3\\\\src\\\\front\\\\app\\\\page.tsx\",\n                    lineNumber: 39,\n                    columnNumber: 9\n                }, this),\n                /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(\"div\", {\n                    className: \"input-container\",\n                    children: [\n                        /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(\"input\", {\n                            type: \"text\",\n                            value: input,\n                            onChange: function(e) {\n                                return setInput(e.target.value);\n                            },\n                            onKeyDown: function(e) {\n                                return e.key === \"Enter\" && sendMessage();\n                            },\n                            className: \"input-field\",\n                            placeholder: \"Type a message...\"\n                        }, void 0, false, {\n                            fileName: \"C:\\\\Users\\\\seohy\\\\Desktop\\\\boostcamp_AITech\\\\LabQ\\\\level4-nlp-finalproject-hackathon-nlp-09-lv3\\\\src\\\\front\\\\app\\\\page.tsx\",\n                            lineNumber: 52,\n                            columnNumber: 11\n                        }, this),\n                        /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(\"button\", {\n                            onClick: sendMessage,\n                            className: \"send-button\",\n                            children: \"Send\"\n                        }, void 0, false, {\n                            fileName: \"C:\\\\Users\\\\seohy\\\\Desktop\\\\boostcamp_AITech\\\\LabQ\\\\level4-nlp-finalproject-hackathon-nlp-09-lv3\\\\src\\\\front\\\\app\\\\page.tsx\",\n                            lineNumber: 60,\n                            columnNumber: 11\n                        }, this)\n                    ]\n                }, void 0, true, {\n                    fileName: \"C:\\\\Users\\\\seohy\\\\Desktop\\\\boostcamp_AITech\\\\LabQ\\\\level4-nlp-finalproject-hackathon-nlp-09-lv3\\\\src\\\\front\\\\app\\\\page.tsx\",\n                    lineNumber: 51,\n                    columnNumber: 9\n                }, this)\n            ]\n        }, void 0, true, {\n            fileName: \"C:\\\\Users\\\\seohy\\\\Desktop\\\\boostcamp_AITech\\\\LabQ\\\\level4-nlp-finalproject-hackathon-nlp-09-lv3\\\\src\\\\front\\\\app\\\\page.tsx\",\n            lineNumber: 37,\n            columnNumber: 7\n        }, this)\n    }, void 0, false, {\n        fileName: \"C:\\\\Users\\\\seohy\\\\Desktop\\\\boostcamp_AITech\\\\LabQ\\\\level4-nlp-finalproject-hackathon-nlp-09-lv3\\\\src\\\\front\\\\app\\\\page.tsx\",\n        lineNumber: 36,\n        columnNumber: 5\n    }, this);\n}\n_s(ChatBot, \"HDAtGPGcvWga1zf1TBXg51T+tsc=\");\n_c = ChatBot;\nvar _c;\n$RefreshReg$(_c, \"ChatBot\");\n\n\n;\n    // Wrapped in an IIFE to avoid polluting the global scope\n    ;\n    (function () {\n        var _a, _b;\n        // Legacy CSS implementations will `eval` browser code in a Node.js context\n        // to extract CSS. For backwards compatibility, we need to check we're in a\n        // browser context before continuing.\n        if (typeof self !== 'undefined' &&\n            // AMP / No-JS mode does not inject these helpers:\n            '$RefreshHelpers$' in self) {\n            // @ts-ignore __webpack_module__ is global\n            var currentExports = module.exports;\n            // @ts-ignore __webpack_module__ is global\n            var prevSignature = (_b = (_a = module.hot.data) === null || _a === void 0 ? void 0 : _a.prevSignature) !== null && _b !== void 0 ? _b : null;\n            // This cannot happen in MainTemplate because the exports mismatch between\n            // templating and execution.\n            self.$RefreshHelpers$.registerExportsForReactRefresh(currentExports, module.id);\n            // A module can be accepted automatically based on its exports, e.g. when\n            // it is a Refresh Boundary.\n            if (self.$RefreshHelpers$.isReactRefreshBoundary(currentExports)) {\n                // Save the previous exports signature on update so we can compare the boundary\n                // signatures. We avoid saving exports themselves since it causes memory leaks (https://github.com/vercel/next.js/pull/53797)\n                module.hot.dispose(function (data) {\n                    data.prevSignature =\n                        self.$RefreshHelpers$.getRefreshBoundarySignature(currentExports);\n                });\n                // Unconditionally accept an update to this module, we'll check if it's\n                // still a Refresh Boundary later.\n                // @ts-ignore importMeta is replaced in the loader\n                module.hot.accept();\n                // This field is set when the previous version of this module was a\n                // Refresh Boundary, letting us know we need to check for invalidation or\n                // enqueue an update.\n                if (prevSignature !== null) {\n                    // A boundary can become ineligible if its exports are incompatible\n                    // with the previous exports.\n                    //\n                    // For example, if you add/remove/change exports, we'll want to\n                    // re-execute the importing modules, and force those components to\n                    // re-render. Similarly, if you convert a class component to a\n                    // function, we want to invalidate the boundary.\n                    if (self.$RefreshHelpers$.shouldInvalidateReactRefreshBoundary(prevSignature, self.$RefreshHelpers$.getRefreshBoundarySignature(currentExports))) {\n                        module.hot.invalidate();\n                    }\n                    else {\n                        self.$RefreshHelpers$.scheduleUpdate();\n                    }\n                }\n            }\n            else {\n                // Since we just executed the code for the module, it's possible that the\n                // new exports made it ineligible for being a boundary.\n                // We only care about the case when we were _previously_ a boundary,\n                // because we already accepted this update (accidental side effect).\n                var isNoLongerABoundary = prevSignature !== null;\n                if (isNoLongerABoundary) {\n                    module.hot.invalidate();\n                }\n            }\n        }\n    })();\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKGFwcC1wYWdlcy1icm93c2VyKS8uL2FwcC9wYWdlLnRzeCIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBRWlDO0FBQ1gsQ0FBQyxnQkFBZ0I7QUFFeEIsU0FBU0M7OztJQUN0QixJQUFnQ0QsWUFBQUEsK0RBQUFBLENBQUFBLCtDQUFRQSxDQUFrQyxFQUFFLE9BQXJFRSxXQUF5QkYsY0FBZkcsY0FBZUg7SUFDaEMsSUFBMEJBLGFBQUFBLCtEQUFBQSxDQUFBQSwrQ0FBUUEsQ0FBQyxTQUE1QkksUUFBbUJKLGVBQVpLLFdBQVlMO0lBRTFCLElBQU1NO21CQUFjO2dCQUdaQyxhQU9BQyxLQUtBQzs7Ozt3QkFkTixJQUFJLENBQUNMLE1BQU1NLElBQUksSUFBSTs7O3dCQUViSCxjQUFjSCxNQUFNTSxJQUFJO3dCQUM5QkwsU0FBUzt3QkFFVCxhQUFhO3dCQUNiRixZQUFZLFNBQUNRO21DQUFTLG9FQUFJQSxhQUFKO2dDQUFVO29DQUFFQyxNQUFNTDtvQ0FBYU0sS0FBSztnQ0FBRzs2QkFBRTs7d0JBR25EOzs0QkFBTUMsTUFBTSxnQkFBZ0I7Z0NBQ3RDQyxRQUFRO2dDQUNSQyxTQUFTO29DQUFFLGdCQUFnQjtnQ0FBbUI7Z0NBQzlDQyxNQUFNQyxLQUFLQyxTQUFTLENBQUM7b0NBQUVDLFNBQVNiO2dDQUFZOzRCQUM5Qzs7O3dCQUpNQyxNQUFNO3dCQUtDOzs0QkFBTUEsSUFBSWEsSUFBSTs7O3dCQUFyQlosT0FBTzt3QkFFYixVQUFVO3dCQUNWTixZQUFZLFNBQUNRO21DQUNYQSxLQUFLVyxHQUFHLENBQUMsU0FBQ0MsS0FBS0M7dUNBQ2JBLFFBQVFiLEtBQUtjLE1BQU0sR0FBRyxJQUFJLHNJQUFLRjtvQ0FBS1YsS0FBS0osS0FBS2lCLFFBQVE7cUNBQUtIOzs7Ozs7OztRQUdqRTt3QkF2Qk1qQjs7OztJQXlCTixxQkFDRSw4REFBQ3FCO1FBQUlDLFdBQVU7a0JBQ2IsNEVBQUNEO1lBQUlDLFdBQVU7OzhCQUNiLDhEQUFDQztvQkFBR0MsT0FBTzt3QkFBRUMsVUFBVTt3QkFBV0MsWUFBWTt3QkFBUUMsV0FBVztvQkFBUzs4QkFBRzs7Ozs7OzhCQUM3RSw4REFBQ047b0JBQUlDLFdBQVU7OEJBQ1oxQixTQUFTb0IsR0FBRyxDQUFDLFNBQUNDLEtBQUtDOzZDQUNsQiw4REFBQ0c7NEJBQWNHLE9BQU87Z0NBQUVJLGNBQWM7NEJBQU07OzhDQUMxQyw4REFBQ0M7b0NBQUVQLFdBQVU7O3NEQUNYLDhEQUFDUTtzREFBTzs7Ozs7O3dDQUFjO3dDQUFFYixJQUFJWCxJQUFJOzs7Ozs7OzhDQUVsQyw4REFBQ3VCO29DQUFFUCxXQUFVOztzREFDWCw4REFBQ1E7c0RBQU87Ozs7Ozt3Q0FBYTt3Q0FBRWIsSUFBSVYsR0FBRyxJQUFJOzs7Ozs7OzsyQkFMNUJXOzs7Ozs7Ozs7Ozs4QkFVZCw4REFBQ0c7b0JBQUlDLFdBQVU7O3NDQUNiLDhEQUFDeEI7NEJBQ0NpQyxNQUFLOzRCQUNMQyxPQUFPbEM7NEJBQ1BtQyxVQUFVLFNBQUNDO3VDQUFNbkMsU0FBU21DLEVBQUVDLE1BQU0sQ0FBQ0gsS0FBSzs7NEJBQ3hDSSxXQUFXLFNBQUNGO3VDQUFNQSxFQUFFRyxHQUFHLEtBQUssV0FBV3JDOzs0QkFDdkNzQixXQUFVOzRCQUNWZ0IsYUFBWTs7Ozs7O3NDQUVkLDhEQUFDQzs0QkFDQ0MsU0FBU3hDOzRCQUNUc0IsV0FBVTtzQ0FDWDs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFPWDtHQWhFd0IzQjtLQUFBQSIsInNvdXJjZXMiOlsid2VicGFjazovL19OX0UvLi9hcHAvcGFnZS50c3g/NzYwMyJdLCJzb3VyY2VzQ29udGVudCI6WyIndXNlIGNsaWVudCc7XHJcblxyXG5pbXBvcnQgeyB1c2VTdGF0ZSB9IGZyb20gJ3JlYWN0JztcclxuaW1wb3J0ICcuL3N0eWxlcy5jc3MnOyAvLyBDU1Mg7YyM7J28IGltcG9ydFxyXG5cclxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gQ2hhdEJvdCgpIHtcclxuICBjb25zdCBbbWVzc2FnZXMsIHNldE1lc3NhZ2VzXSA9IHVzZVN0YXRlPHsgdXNlcjogc3RyaW5nOyBib3Q6IHN0cmluZyB9W10+KFtdKTtcclxuICBjb25zdCBbaW5wdXQsIHNldElucHV0XSA9IHVzZVN0YXRlKCcnKTtcclxuXHJcbiAgY29uc3Qgc2VuZE1lc3NhZ2UgPSBhc3luYyAoKSA9PiB7XHJcbiAgICBpZiAoIWlucHV0LnRyaW0oKSkgcmV0dXJuO1xyXG5cclxuICAgIGNvbnN0IHVzZXJNZXNzYWdlID0gaW5wdXQudHJpbSgpO1xyXG4gICAgc2V0SW5wdXQoJycpO1xyXG5cclxuICAgIC8vIOyCrOyaqeyekCDrqZTsi5zsp4Ag7LaU6rCAXHJcbiAgICBzZXRNZXNzYWdlcygocHJldikgPT4gWy4uLnByZXYsIHsgdXNlcjogdXNlck1lc3NhZ2UsIGJvdDogJycgfV0pO1xyXG5cclxuICAgIC8vIEFQSSDtmLjstpxcclxuICAgIGNvbnN0IHJlcyA9IGF3YWl0IGZldGNoKCcvYXBpL2NoYXRib3QnLCB7XHJcbiAgICAgIG1ldGhvZDogJ1BPU1QnLFxyXG4gICAgICBoZWFkZXJzOiB7ICdDb250ZW50LVR5cGUnOiAnYXBwbGljYXRpb24vanNvbicgfSxcclxuICAgICAgYm9keTogSlNPTi5zdHJpbmdpZnkoeyBtZXNzYWdlOiB1c2VyTWVzc2FnZSB9KSxcclxuICAgIH0pO1xyXG4gICAgY29uc3QgZGF0YSA9IGF3YWl0IHJlcy5qc29uKCk7XHJcblxyXG4gICAgLy8g67SHIOydkeuLtSDstpTqsIBcclxuICAgIHNldE1lc3NhZ2VzKChwcmV2KSA9PlxyXG4gICAgICBwcmV2Lm1hcCgobXNnLCBpZHgpID0+XHJcbiAgICAgICAgaWR4ID09PSBwcmV2Lmxlbmd0aCAtIDEgPyB7IC4uLm1zZywgYm90OiBkYXRhLnJlc3BvbnNlIH0gOiBtc2dcclxuICAgICAgKVxyXG4gICAgKTtcclxuICB9O1xyXG5cclxuICByZXR1cm4gKFxyXG4gICAgPGRpdiBjbGFzc05hbWU9XCJjb250YWluZXJcIj5cclxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJjaGF0LWJveFwiPlxyXG4gICAgICAgIDxoMSBzdHlsZT17eyBmb250U2l6ZTogJzEuMjVyZW0nLCBmb250V2VpZ2h0OiAnYm9sZCcsIHRleHRBbGlnbjogJ2NlbnRlcicgfX0+Q2hhdEJvdDwvaDE+XHJcbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtZXNzYWdlLWNvbnRhaW5lclwiPlxyXG4gICAgICAgICAge21lc3NhZ2VzLm1hcCgobXNnLCBpZHgpID0+IChcclxuICAgICAgICAgICAgPGRpdiBrZXk9e2lkeH0gc3R5bGU9e3sgbWFyZ2luQm90dG9tOiAnOHB4JyB9fT5cclxuICAgICAgICAgICAgICA8cCBjbGFzc05hbWU9XCJ1c2VyLW1lc3NhZ2VcIj5cclxuICAgICAgICAgICAgICAgIDxzdHJvbmc+VXNlcjo8L3N0cm9uZz4ge21zZy51c2VyfVxyXG4gICAgICAgICAgICAgIDwvcD5cclxuICAgICAgICAgICAgICA8cCBjbGFzc05hbWU9XCJib3QtbWVzc2FnZVwiPlxyXG4gICAgICAgICAgICAgICAgPHN0cm9uZz5Cb3Q6PC9zdHJvbmc+IHttc2cuYm90IHx8ICdUeXBpbmcuLi4nfVxyXG4gICAgICAgICAgICAgIDwvcD5cclxuICAgICAgICAgICAgPC9kaXY+XHJcbiAgICAgICAgICApKX1cclxuICAgICAgICA8L2Rpdj5cclxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImlucHV0LWNvbnRhaW5lclwiPlxyXG4gICAgICAgICAgPGlucHV0XHJcbiAgICAgICAgICAgIHR5cGU9XCJ0ZXh0XCJcclxuICAgICAgICAgICAgdmFsdWU9e2lucHV0fVxyXG4gICAgICAgICAgICBvbkNoYW5nZT17KGUpID0+IHNldElucHV0KGUudGFyZ2V0LnZhbHVlKX1cclxuICAgICAgICAgICAgb25LZXlEb3duPXsoZSkgPT4gZS5rZXkgPT09ICdFbnRlcicgJiYgc2VuZE1lc3NhZ2UoKX1cclxuICAgICAgICAgICAgY2xhc3NOYW1lPVwiaW5wdXQtZmllbGRcIlxyXG4gICAgICAgICAgICBwbGFjZWhvbGRlcj1cIlR5cGUgYSBtZXNzYWdlLi4uXCJcclxuICAgICAgICAgIC8+XHJcbiAgICAgICAgICA8YnV0dG9uXHJcbiAgICAgICAgICAgIG9uQ2xpY2s9e3NlbmRNZXNzYWdlfVxyXG4gICAgICAgICAgICBjbGFzc05hbWU9XCJzZW5kLWJ1dHRvblwiXHJcbiAgICAgICAgICA+XHJcbiAgICAgICAgICAgIFNlbmRcclxuICAgICAgICAgIDwvYnV0dG9uPlxyXG4gICAgICAgIDwvZGl2PlxyXG4gICAgICA8L2Rpdj5cclxuICAgIDwvZGl2PlxyXG4gICk7XHJcbn1cclxuIl0sIm5hbWVzIjpbInVzZVN0YXRlIiwiQ2hhdEJvdCIsIm1lc3NhZ2VzIiwic2V0TWVzc2FnZXMiLCJpbnB1dCIsInNldElucHV0Iiwic2VuZE1lc3NhZ2UiLCJ1c2VyTWVzc2FnZSIsInJlcyIsImRhdGEiLCJ0cmltIiwicHJldiIsInVzZXIiLCJib3QiLCJmZXRjaCIsIm1ldGhvZCIsImhlYWRlcnMiLCJib2R5IiwiSlNPTiIsInN0cmluZ2lmeSIsIm1lc3NhZ2UiLCJqc29uIiwibWFwIiwibXNnIiwiaWR4IiwibGVuZ3RoIiwicmVzcG9uc2UiLCJkaXYiLCJjbGFzc05hbWUiLCJoMSIsInN0eWxlIiwiZm9udFNpemUiLCJmb250V2VpZ2h0IiwidGV4dEFsaWduIiwibWFyZ2luQm90dG9tIiwicCIsInN0cm9uZyIsInR5cGUiLCJ2YWx1ZSIsIm9uQ2hhbmdlIiwiZSIsInRhcmdldCIsIm9uS2V5RG93biIsImtleSIsInBsYWNlaG9sZGVyIiwiYnV0dG9uIiwib25DbGljayJdLCJzb3VyY2VSb290IjoiIn0=\n//# sourceURL=webpack-internal:///(app-pages-browser)/./app/page.tsx\n"));

/***/ })

});