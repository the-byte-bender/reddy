# Simple thread pool that can have functions submitted and it will call the spesified callback when the function finish's executing, in the main thread.
import typing
from concurrent.futures import Future, ThreadPoolExecutor
import wx

threadpool = ThreadPoolExecutor(2)
callback_type = typing.Callable[[typing.Any], None]


def submit(
    func: typing.Callable,
    callback: typing.Optional[
        typing.Union[callback_type, typing.Iterable[callback_type]]
    ],
    *args,
    **kwargs
):
    future: Future = threadpool.submit(func, *args, **kwargs)
    if callback:
        if callable(callback):
            future.add_done_callback(wrap(callback))
        else:
            for cb in callback:
                future.add_done_callback(wrap(cb))


def wrap(func: callback_type):
    return lambda f: wx.CallAfter(func, f.result())
