[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)

## The tools I use in my daily life


---
## Logger

This is a new module, I have not worked on it a lot yet, feel free to contribute to add more features or improve my code !

The Logger is a collection of classes and wrapper that provides a simple way to `log` messages to the console with different `colors` and `format`.

The module currently contains the following classes:
- `ColorCodes` - A dataclass that contains the `color value` for the logger.
- `ConsoleFormatter` - A class that `format` and `color` to the `console`.
  - It also contains a wrapper that I called the `Watcher` 
- `FileFormatter` - A class that `format` and output to a `file`.


### Example

```python
from logger import init_logging

logger = init_logging("My Logger", "DEBUG", "log.log")

logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```

As you can see, the Logger uses the `logging` module behind the scene so most of the it's functions should work fine.

<img src="https://github.com/abedaton/tools/blob/main/img/logger_result.png" width=40%>