from inspect import signature, Parameter

class WTFError(BaseException):
    pass


def churried(explicit=False, auto_restore=True):
    def wrapper(func):
        sig = signature(func)

        class _churrier:
            def __init__(self):
                self.sig = sig

                self._internal = func

                self._states = []

                self._initialize()

            def push_state(self):
                self._states.append((
                    self._defaults.copy(),
                    self._keyword_args.copy(),
                    self._positional_args.copy(),
                    self._filled_args.copy(),
                    self._args.copy(),
                    self._kwargs.copy(),
                    self._has_var_positional_arg,
                    self._has_var_keyword_arg
                ))

                return self

            freeze = push_state

            def pop_state(self):
                (self._defaults,
                 self._keyword_args,
                 self._positional_args,
                 self._filled_args,
                 self._args,
                 self._kwargs,
                 self._has_var_positional_arg,
                 self._has_var_keyword_arg) = self._states.pop()

                return self

            restore = pop_state

            def _initialize(self):
                self._defaults = {}
                self._keyword_args = set()
                self._positional_args = []
                self._filled_args = set()

                self._args = []
                self._kwargs = {}

                self._has_var_positional_arg = explicit or False
                self._has_var_keyword_arg = False

                for n, v in self.sig.parameters.items():
                    if v.kind == Parameter.KEYWORD_ONLY:
                        self._defaults[n] = v.default
                        self._keyword_args.add(n)

                    elif v.kind == Parameter.POSITIONAL_OR_KEYWORD:
                        self._defaults[n] = v.default
                        if v.default == Parameter.empty:
                            self._positional_args.append(n)
                        else:
                            self._keyword_args.add(n)

                    elif v.kind == Parameter.VAR_POSITIONAL:
                        self._has_var_positional_arg = True

                    elif v.kind == Parameter.VAR_KEYWORD:
                        self._has_var_keyword_arg = True

                    else:
                        raise WTFError('How do you manage to declare '
                                       'a positional-only argument '
                                       'in plain Python?')

                self._kwargs.update(**{k: v
                                       for k, v in self._defaults.items()
                                       if v != Parameter.empty})

            def _evaluate(self):
                ret = self._internal(*self._args, **self._kwargs)

                self._initialize()

                if auto_restore:
                    if self._states:
                        self.restore()

                return ret

            def __call__(self, *args, **kwargs):
                self._args.extend(args)
                self._kwargs.update(kwargs)

                if (not args) and (not kwargs):
                    return self._evaluate()

                if self._has_var_positional_arg:
                    return self
                else:
                    for _ in range(len(args)):
                        if self._positional_args:
                            self._filled_args.add(self._positional_args.pop(0))

                if self._has_var_keyword_arg:
                    return self
                else:
                    for k, v in kwargs.items():
                        if k in self._filled_args:
                            continue
                        if k in self._positional_args:
                            self._filled_args.add(k)
                            self._positional_args.remove(k)
                        else:
                            self._filled_args.add(k)
                            self._keyword_args.remove(k)

                if not self._positional_args:
                    return self._evaluate()

                return self

            def __getattr__(self, item):
                if item not in self.sig.parameters:
                    if self._has_var_keyword_arg:
                        def _(x):
                            return self(**{item: x})
                        return _

                    raise TypeError("%s() got an unexpected "
                                    "keyword argument '%s'" %
                                    (self._internal.__name__, item))

                def _(x=self._defaults[item]):
                    return self(**{item: x})

                return _
        return _churrier()

    return wrapper
