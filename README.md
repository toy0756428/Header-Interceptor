# Burp Extension - Header Interceptor with Selenium

This extension uses **Selenium for simulating page input** and **HTTP Header filtering functionality** to intercept and view specific request headers.

## Requirements

- Burp Suite (Pro or Community Edition)
- **Jython 2.7.x**
- **Python 3.x** (used by the Selenium script)
- Required packages:
  - [selenium](https://pypi.org/project/selenium/)
  - Corresponding browser drivers (e.g., ChromeDriver)
 
## Use

- **Burp proxy**: 127.0.0.1:8088
- **Selenium Script Configuration**: Customize the input data and interaction through the `selenium_task` settings.
- **Header Interceptor Settings**: Configure the Python interpreter and `selenium_script.py` path for automation execution.
