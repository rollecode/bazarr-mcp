### 1.1.0: 2026-10-02

* Page results larger than 20 000 tokens
* Add get_result_page to page, filter and narrow them
* Parse JSON bodies containing invalid UTF-8

### 1.0.2: 2026-09-28

* Keep idle sessions for 24 hours

### 1.0.1: 2026-09-19

* Report its own name, not Cronometer's

### 1.0.0: 2026-09-15

* Every Bazarr API operation as a tool
* Spec extracted from Bazarr's flask_restx decorators
* Form-encoded fields, as Bazarr expects
* Coverage test compares tools against the spec