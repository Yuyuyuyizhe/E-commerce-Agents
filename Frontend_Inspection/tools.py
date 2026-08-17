import asyncio
from datetime import datetime, timedelta
import json


def _scale_point(x: float, y: float, width: int, height: int) -> tuple[int, int]:
    sx = max(0, min(1000, x)) / 1000.0
    sy = max(0, min(1000, y)) / 1000.0
    return int(sx * width), int(sy * height)


async def _device_call(func, /, *args, **kwargs):
    return await asyncio.to_thread(func, *args, **kwargs)


async def _device_click(device: Device, x: float, y: float):
    return await _device_call(device.click, x, y)


async def _device_window_size(device: Device):
    return await _device_call(device.window_size)


async def _device_input_text(device: Device, text: str) -> None:
    await _device_call(device.clear_text)
    await _device_call(device.set_fastinput_ime, True)
    try:
        await _device_call(device.send_keys, text)
    finally:
        await _device_call(device.set_fastinput_ime, False)


@register
@should_record
@tool
async def mobile_get_live_room_id(rt: ToolRuntime[AgentContext]):
    """
    当你第一次点进一个直播房间，获取直播房间 ID
    """
    try:
        live_room_id = await _resolve_live_room_id(rt)
    except ValueError as e:
        return str(e)
    return f"当前直播间 ID 为：{live_room_id}"


@register
@tool
async def mobile_input_text(rt: ToolRuntime[AgentContext], text: str):
    """
    输入文本
    """
    mobile = get_mobile(rt)
    await _device_input_text(mobile.device, text)
    return f"已输入文本: {text}"


@register
@tool
async def mobile_tap(
    rt: ToolRuntime[AgentContext],
    x: Annotated[float, "点击屏幕的x坐标"],
    y: Annotated[float, "点击屏幕的y坐标"],
):
    """
    点击屏幕指定坐标范围
    """
    mobile = get_mobile(rt)
    width, height = await _device_window_size(mobile.device)
    ax, ay = _scale_point(x, y, width, height)
    await _device_click(mobile.device, ax, ay)
    await asyncio.sleep(interval)
    await _device_click(mobile.device, ax, ay)
    return f"双击了屏幕坐标范围 {ax}, {ay}"


@register
@tool
async def mobile_double_tap(
    rt: ToolRuntime[AgentContext],
    x: Annotated[float, "点击屏幕的x坐标"],
    y: Annotated[float, "点击屏幕的y坐标"],
    interval: Annotated[float, "双击间隔时间"] = 0.1,
):
):
    """
    双击屏幕指定坐标范围
    """
    mobile = get_mobile(rt)
    width, height = await _device_window_size(mobile.device)
    ax, ay = _scale_point(x, y, width, height)
    await _device_click(mobile.device, ax, ay)
    return f"双击了屏幕坐标范围 {ax}, {ay}"


@register
@tool
async def mobile_back(rt: ToolRuntime[AgentContext]):
    """
    点击返回键
    """
    mobile = get_mobile(rt)
    await _device_press(mobile.device, "back")
    return "点击了返回"


@register
@tool
async def mobile_swipe_up(
    rt: ToolRuntime[AgentContext],
    scale: Annotated[float] = 0.8,
):
    """
    向上滑动，用于看下方未展示的内容，或者切换到下一个视频、直播间
    """
    mobile = get_mobile(rt)
    await asyncio.to_thread(mobile.device.swipe_ext, "up", scale=scale, duration=0.05)
    return f"向上滑动了{scale}"


@register
@tool
async def mobile_swipe_down(
    rt: ToolRuntime[AgentContext],
    scale: Annotated[float] = 0.8,
):
    """
    向下滑动，用于看上方未展示的内容，或者切换到上一个视频、直播间
    """
    mobile = get_mobile(rt)
    await asyncio.to_thread(mobile.device.swipe_ext, "down", scale=scale)
    return f"向下滑动了{scale}"


@register
@tool
async def mobile_set_device_and_lauch_douyin(
    rt: ToolRuntime[AgentContext],
    tags: Annotated[
        list[str],
        "云手机设备标签列表"
    ] = None,
):
    """
    设置云手机设备标签并启动抖音应用
    """
    required_tags = _normalize_cloud_phone_tags(tags)
    mobile = await _set_context_mobile_from_pool(rt, required_tags=required_tags)
    if not required_tags:
        return format_mobile_pool_lauch_message(mobile, rt.context.trace_id)

    trace_id = rt.context.trace_id
    trace_url = f"https://fornax.bytedance.net/space/7590080701171019522/analytics/trace/{trace_id}"
    return (
        f"设备 {mobile} 已初始化，当前回话调用链: {trace_url}"
    )

