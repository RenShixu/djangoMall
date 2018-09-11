from PIL import Image
import time,os
def picupload(request):
    '''
    图片上传
    :param request:
    :return: 图片名称
    '''
    picname = 0
    try:
        picfile = request.FILES.get("pic")
        if picfile:
            picname = str(time.time()) + "." + picfile.name.split(".").pop()
            destination = open("./static/goods/" + picname, "+wb")
            for chunk in picfile.chunks():
                destination.write(chunk)
            destination.close()

            # 图片的缩放
            im = Image.open("./static/goods/" + picname)
            # 缩放到375*375(缩放后的宽高比例不变):
            im.thumbnail((375, 375))
            im.save("./static/goods/" + picname, None)

            im = Image.open("./static/goods/" + picname)
            # 缩放到220*220(缩放后的宽高比例不变):
            im.thumbnail((220, 220))
            im.save("./static/goods/m_" + picname, None)

            im = Image.open("./static/goods/" + picname)
            # 缩放到75*75(缩放后的宽高比例不变):
            im.thumbnail((75, 75))
            im.save("./static/goods/s_" + picname, None)
        else:
            picname = "请选择图片"
    except Exception as err:
        print("文件上传异常：{}",err)
    return picname

def deletepic(picname):
    '''
    删除服务器上的图片
    :param picname:
    :return:
    '''
    if os.path.exists("./static/goods/" + picname):
        os.remove("./static/goods/" + picname)
    if os.path.exists("./static/goods/s_" + picname):
        os.remove("./static/goods/s_" + picname)
    if os.path.exists("./static/goods/m_" + picname):
        os.remove("./static/goods/m_" + picname)