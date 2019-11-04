class Res(object):
    # TCP配置
    tcpClientAddress = (r"", 6001)
    tcpServerAddress = (r"182.61.3.51", 6000)
    # UI配置
    mainWindowIcon = r"Res/Icon/drone_128px.png"

    # 百度地图
    mapUrl = r"/Res/HTML/Map.html"

    # 全局变量
    upload = {'cmd': 'upload'}
    download = {'cmd': 'download'}
    update = {'cmd': 'update'}

    tasks = []
    events = []
