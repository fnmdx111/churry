from functools import partial
from unittest import TestCase, main
from churry import churried


class TestChurry(TestCase):
    def setUp(self):
        @churried()
        def _(a, b, *args, c='c', d='d', **kwargs):
            return a, b, args, c, d, kwargs

        self.test_func1 = _

        @churried()
        def _(a, b, *args, c='c', d='d'):
            return a, b, args, c, d

        self.test_func2 = _

        @churried()
        def _(a, b, c='c', d='d', **kwargs):
            return a, b, c, d, kwargs

        self.test_func3 = _

        @churried(auto_restore=True)
        def _(a, b, c='c', d='d'):
            return a, b, c, d

        self.test_func4 = _

        @churried()
        def _(a, b, *, c='c', d='d'):
            return a, b, c, d

        self.test_func5 = _

        @churried(explicit=True)
        def _(a, b, *, c='c', d='d'):
            return a, b, c, d

        self.test_func6 = _

        self.bind_result = lambda r: partial(self.assertEqual, r)

    def test_1(self):
        _ = self.bind_result((1, 2, (3, 4), 5, 'd', {'e': 6}))

        _(self.test_func1(1, 2, 3, 4).c(5).e(6)())
        _(self.test_func1(1, 2, e=6).c(5)(3, 4)())
        _(self.test_func1(1, 2).e(6)(3).c(5)(4)())

    def test_2(self):
        _ = self.bind_result((1, 2, (3, 4), 5, 'e'))

        _(self.test_func2(1, 2, 3, 4).c(5).d('e')())
        _(self.test_func2(1, 2, 3, d='e').c(5)(4)())
        _(self.test_func2(1, 2).d('e')(3).c(5)(4)())

        with self.assertRaises(TypeError):
            _(self.test_func2(1, 2, 3).c(5, d='e')())

    def test_3(self):
        _ = self.bind_result((1, 2, 5, 'e', {'e': 6, 'f': 7}))

        _(self.test_func3(1, 2, c=5).d('e').e(6).f(7)())
        _(self.test_func3(1, e=6)(2).d('e').c(5).f(7)())
        _(self.test_func3(e=6, f=7).d('e').c(5)(1, 2)())

    def test_4(self):
        _ = self.bind_result((1, 2, 3, 4))

        x = self.test_func4(1).c(3).d(4).freeze()
        _(x(2))
        _(x(2))
        _(self.test_func4(a=1).c(3).d(4).b(2))
        _(self.test_func4.b(2).c(3).d(4).a(1))

    def test_5(self):
        _ = self.bind_result((1, 2, 3, 4))

        _(self.test_func4(1).c(3).d(4)(2))
        _(self.test_func4(a=1).c(3).d(4).b(2))
        _(self.test_func4.b(2).c(3).d(4).a(1))

    def test_6(self):
        _ = self.bind_result((1, 2, 3, 4))

        _(self.test_func6(1, 2).c(3).d(4)())
        _(self.test_func6.a(1).b(2).c(3).d(4)())
        _(self.test_func6(c=3, d=4)(1).b(2)())


if __name__ == '__main__':
    main()
