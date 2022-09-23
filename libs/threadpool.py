# Simple thread pool that can have functions submitted and it will call the spesified callback when the function finish's executing, in the main thread.
import typing
from concurrent.futures import Future, ThreadPoolExecutor
from gi.repository import GObject

pools = [ThreadPoolExecutor(max_workers=2), ThreadPoolExecutor(max_workers=2)]
callback_type = typing.Callable[[typing.Any], None]


def submit(
    func: typing.Callable,
    callback: typing.Optional[
        typing.Union[callback_type, typing.Iterable[callback_type]]
    ],
    *args,
    **kwargs
):
    threadpool = pools[kwargs.get("threadpool", 0)]
    if "threadpool" in kwargs:
        del kwargs["threadpool"]
    def wrapped_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
    future: Future = threadpool.submit(wrapped_func, *args, **kwargs)
    if callback:
        if callable(callback):
            future.add_done_callback(wrap(callback))
        else:
            for cb in callback:
                future.add_done_callback(wrap(cb))
        return future


def wrap(func: callback_type):
    return lambda f: GObject.idle_add(func, f.result())
