from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import sys
from PIL import Image
global dance,pos,v,angle
yrotate=0
class PartState:#ЦВЕТА
    def __init__(self,tx,ty,tz,sx,sy,sz,rx,ry,rz,color):
        self.tx=tx
        self.ty=ty
        self.tz=tz
        self.sx=sx
        self.sy=sy
        self.sz=sz
        self.rx=rx
        self.ry=ry
        self.rz=rz
        self.color = color

class View:#КООРДИНАТЫ
    def __init__(self,eyeX,eyeY,eyeZ,centerX,centerY,centerZ,upX,upY,upZ):
        self.eyeX = eyeX
        self.eyeY = eyeY
        self.eyeZ = eyeZ
        self.centerX = centerX
        self.centerY = centerY
        self.centerZ = centerZ
        self.upX = upX
        self.upY = upY
        self.upZ = upZ

global trunk,head#ГОЛОВА И ТЕЛО
global larm,lfarm,rarm,rfarm#РУКИ
global luleg,llleg,ruleg,rlleg#НОГИ




   
def drawCube(wall_mat):#СЦЕНА
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, wall_mat)
    glBegin(GL_QUADS)
    # left wall */    
    glNormal3f(-1, 0, 0)#Для создания корректного освещения сцены нужно правильно установить нормали. Они задаются для вершин полигонов командой
    #glNormal3f(GLfloat nx, GLfloat ny, GLfloat nz);
#glNormal3fv(const GLfloat *v);
#
#нормаль должна быть перпендикулярна к поверхности в данной вершине;
#нормаль задается для лицевой стороны поверхности;
#нормаль должна иметь единичную длину. Приведение нормалей к единичной длине можно поручить OpenGL командой:
#glEnable(GL_NORMALIZE);
#GL_POINTS — каждая вершина задает точку
#GL_LINES — каждая отдельная пара вершин задает линию
#GL_LINE_STRIP — каждая пара вершин задает линию (т.е. конец предыдущей линии является началом следующей)
#GL_LINE_LOOP — аналогично предыдущему за исключением того, что последняя вершина соединяется с первой и получается замкнутая фигура
#GL_TRIANGLES — каждая отдельная тройка вершин задает треугольник
#GL_TRIANGLE_STRIP — каждая следующая вершина задает треугольник вместе с двумя предыдущими (получается лента из треугольников)
#GL_TRIANGLE_FAN — каждый треугольник задается первой вершиной и последующими парами (т.е. треугольники строятся вокруг первой вершины, образуя нечто похожее на диафрагму)
#GL_QUADS — каждые четыре вершины образуют четырехугольник
#GL_QUAD_STRIP — каждая следующая пара вершин образует четырехугольник вместе с парой предыдущих
#GL_POLYGON — задает многоугольник с количеством углов равным количеству заданных вершин
    glVertex3f(-1, -1,  1)
    glVertex3f(-1,  1,  1)
    glVertex3f(-1,  1, -1)
    glVertex3f(-1, -1, -1)
    # right wall 
    glNormal3f(1, 0, 0)
    glVertex3f( 1, -1,  1)
    glVertex3f( 1, -1, -1)
    glVertex3f( 1,  1, -1)
    glVertex3f( 1,  1,  1)
    # ceiling 
    glNormal3f(0, 1, 0)
    glVertex3f(-1,  1,  1)
    glVertex3f( 1,  1,  1)
    glVertex3f( 1,  1, -1)
    glVertex3f(-1,  1, -1)
    # back wall 
    glNormal3f(0, 0, -1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1,  1, -1)
    glVertex3f( 1,  1, -1)
    glVertex3f( 1, -1, -1)
    #floor
    glNormal3f(0, -1, 0)
    glVertex3f(-1, -1,  1)
    glVertex3f(-1, -1, -1)
    glVertex3f( 1, -1, -1)
    glVertex3f( 1, -1,  1)
    #front wall
    glNormal3f(0, 0, 1)
    glVertex3f(-1, -1,  1)
    glVertex3f( 1, -1,  1)
    glVertex3f( 1,  1,  1)
    glVertex3f(-1,  1,  1)
    glEnd()#КОНЕЦ

def resize(w, h):
    glViewport(0, 0, w , h)#Viewport - это область окна, в которой будет отображаться результаты нашей работы. Для установки области видимости надо использовать функцию OpenGL glViewport(GLint x, GLint y, GLsizei width, GLsizei height).
    glMatrixMode(GL_PROJECTION)#все последующие изменения будут применяться к проекционной матрице.
    glLoadIdentity()#текущая матрица будет сделана единичной.
    gluPerspective(60.0, float(w)/float(h), 10.0, 1000.0)#Создает матрицу для пирамиды симметричного перспективного вида и умножает на нее текущую матрицу. Параметр fovy задает угол визуального охвата в плоскости yz, его значение должно лежать в диапазоне [0.0, 180.0].
    glMatrixMode(GL_MODELVIEW)#все последующие изменения будут применяться к объектно-видовой матрице.
    
                 
def init():
    glEnable(GL_DEPTH_TEST)#glEnable(GL_DEPTH_TEST); После включения OpenGL автоматически сохраняет фрагменты, если их z-значения в буфере глубины прошли тест глубины, и отбрасывает те фрагменты, которые не прошли тест глубины.
    glEnable(GL_LIGHTING)#СВЕТ
    glEnable(GL_LIGHT0)#СВЕТ1
    glEnable(GL_LIGHT4)#СВЕТ4

    glClearColor(57, 255, 25, 0.5)#ЦВЕТ ФОНА
    glShadeModel(GL_SMOOTH)#Режим сглаживания по умолчанию разрешен. Он переключается функцией glShadeModel с аргументами GL_FLAT и GL_SMOOTH. 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)#GL_COLOR_BUFFER_BIT	Очистка буфера цвета GL_DEPTH_BUFFER_BIT	Очистка буфера глубины. GL_ACCUM_BUFFER_BIT	Очистка буфера накопления. GL_STENCIL_BUFFER_BIT	Очистка буфера трафарета.
    glLightfv(GL_LIGHT4,GL_POSITION,(220,220,220))#СВЕТ
    
    
    #ПРОИЗВОДИМ НАСТРОЙКИ ЦВЕТА, ДЛЯ СОЗДАНИЯ БЛИКА - ИЛИ ЗЕРКАЛЬНОГО ОТРАЖЕНИЯ.
    blick = [ 1.0, 1.0, 1.0, 1.0 ]#ЗАДАНИЕ ПАРАМЕТРОВ БЛИКА
    glMaterialfv(GL_FRONT, GL_SPECULAR, blick)
    glLightfv(GL_LIGHT0, GL_SPECULAR, blick)
    glMateriali(GL_FRONT, GL_SHININESS, 100)
    
    
    
    
    global yrotate
    global dance
    global pos
    global v
    global trunk,head
    global larm,lfarm,rarm,rfarm
    global luleg,llleg,ruleg,rlleg
    pos = 0
    v = View(15,15,15,0,0,0,0,1,0)
    trunk = PartState(0,0,0, 5  ,7  ,2.5,0,0,0,(0,0,1,0.0))
    head = PartState(0,0,0, 1.6,2  ,2  ,0,0,0,(0,1,0,0.2))
    larm = PartState(0,0,0, 1.2,3.5,1.5,0,0,0,(1,0,0,0.2))
    lfarm = PartState(0,0,0, 1.0,3.0,1.0,0,0,0,(1,0.5,0,0.2))
    rarm = PartState(0,0,0, 1.2,3.5,1.5,0,0,0,(1,0,0,0.2))
    rfarm = PartState(0,0,0, 1.0,3.0,1.0,0,0,0,(1,0.5,0,0.2))
    luleg = PartState(0,0,0, 1.1,3.0,2  ,0,0,0,(0,0,1,0.2))
    llleg = PartState(0,0,0, 0.9,4.5,1.8,0,0,0,(0,0,1,0.2))
    ruleg = PartState(0,0,0, 1.1,3.0,2  ,0,0,0,(0,0,1,0.2))
    rlleg = PartState(0,0,0, 0.9,4.5,1.8,0,0,0,(0,0,1,0.2))
    
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)#Очистка сцены
    #glColor4f(0,0,1,0)
    #v = View(0,0,35,0,0,0,0,1,0)
    glMatrixMode(GL_MODELVIEW)#все последующие изменения будут применяться к объектно-видовой матрице.
    glLoadIdentity()#/ Сброс просмотра
    glPushMatrix()#•	glPushMatrix(), glPopMatrix() - с помощью этих команд мы можем сохранять и восстанавливать матрицы соответственно
    gluLookAt(v.eyeX,v.eyeY,v.eyeZ,v.centerX,v.centerY,v.centerZ,v.upX,v.upY,v.upZ)#камера
    global trunk
    #hierarchy modelling
    
    glTranslatef(trunk.tx,trunk.ty,trunk.tz)#поворот
    glRotatef(trunk.ry+45,0,1,0)#объект будет поварачиваться на 10 градусов по оси Y.
   # glTranslatef(-10,-10,-10)
    #НАПИСАТЬ ФУНКЦИЮ СЦЕНЫ
    drawHead()
    drawTrunk()
    drawArms() 
    drawLegs()
    drawScene()
    glPopMatrix()
    glutSwapBuffers()#glutSwapBuffers меняет местами буферы текущего окна, если они дважды буферизованы.

def drawTrunk():
    glPushMatrix()
    glScalef(trunk.sx,trunk.sy,trunk.sz)
    wall_mat = (1.0, 1.0, 1.0, 0.0)
    drawCube(wall_mat)
    glPopMatrix()    

    
def drawHead():
    glPushMatrix()
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, 0,0,0, 0.9,4.5,1.8,0,0,0,(0,0,1,0.2))
    glTranslatef(0.1,9,0.1)
    glutSolidSphere(2,22,22)

    glPushMatrix()#eyeL
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, 11,11,11,0)
    glTranslatef(-0.5,0.2,1.1)
    glutSolidSphere(1.0,11,11)
    glPopMatrix()

    glPushMatrix()#eyeR
    glTranslatef(0.5,0.2,1.1)
    glutSolidSphere(1.0,11,11)
    glPopMatrix()    
    glPopMatrix()



def draw_cube(x, y, z):
    glPushMatrix()
    glTranslatef(-x / 2, -y / 2, -z / 2)
   
    glBegin(GL_QUADS)
    
    # near
    
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x, 0, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x, y, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, y, 0)
    # far
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, y, z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x, y, z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x, 0, z)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, z)
    # left
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, y, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(0, y, z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(0, 0, z)
    # right
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, 0, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x, y, z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x, 0, z)

    # bottom
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x, 0, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x, 0, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, 0, z)

    # top
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, y, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x, y, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x, y, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, y, z)
    glEnd()
    glPopMatrix()

def drawScene():
    
    #низ
    niz=load_texture("1.jpg")
    

    
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, niz)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_COLOR_MATERIAL)
    glColor3f(255,255,255)
    glTranslatef(0, -21, 0.5)
    glRotate(90, 10, 0, 0.0)
    draw_cube(200, 150, 6)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    



    # зад
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, niz)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_COLOR_MATERIAL)
    glTranslatef(0, 40, -72)
    draw_cube(200, 150, 6)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()







    # правая стенка
    #glBindTexture(GL_TEXTURE_2D, potolok_texture)
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, niz)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_COLOR_MATERIAL)
    glTranslatef(90, 40, 0)
    glRotate(90, 0, 10, 0)
    draw_cube(150, 150, 6)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()





    #glDisable(GL_TEXTURE_2D)
    # левая стенка
    glPushMatrix()
    
    glBindTexture(GL_TEXTURE_2D, niz)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_COLOR_MATERIAL)
    glTranslatef(-90, 40, 0)
    glRotate(90, 0, 10, 0)
    draw_cube(150, 150, 6)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

    #лицевая стена
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, niz)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_COLOR_MATERIAL)
    glTranslatef(0, 40, 72)
    draw_cube(200, 150, 6)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

    





def drawArms():
    
    global larm #left Arm
    glPushMatrix() #start larm
    glTranslatef(-(trunk.sx+larm.sx),trunk.sy,0)
    glRotatef(larm.rx,1,0,0)
    glTranslatef(0,-larm.sy,0)
    glPushMatrix() #start Scaling
    glScalef(larm.sx,larm.sy,larm.sz)
    wall_mat = (larm.color[0],larm.color[1],larm.color[2],0)
    drawCube(wall_mat)
    glPopMatrix() #end Scaling

    
    global lfarm #lfarm
    glPushMatrix() #start lfarm
    glTranslatef(0,-(larm.sy),0)
    glRotatef(lfarm.rx,1,0,0)
    glTranslatef(0,-lfarm.sy,0)
    glPushMatrix() #start Scaling
    glScalef(lfarm.sx,lfarm.sy,lfarm.sz) 
    wall_mat = (lfarm.color[0],lfarm.color[1],lfarm.color[2],0)
    drawCube(wall_mat)
    glPopMatrix() #end Scaling
    glPopMatrix() #end lfarm
    glPopMatrix() #end left Arms

    
    global rarm #right arm
    glPushMatrix() #start right arm
    glTranslatef(trunk.sx+rarm.sx,trunk.sy,0)
    glRotatef(rarm.rx,1,0,0)
    glTranslatef(0,-rarm.sy,0)
    glPushMatrix() #start scaling
    glScalef(rarm.sx,rarm.sy,rarm.sz)
    wall_mat = (rarm.color[0],rarm.color[1],rarm.color[2],0)
    drawCube(wall_mat)
    glPopMatrix() #end Scaling

    
    global rfarm #right Fore Arm
    glPushMatrix() #start rfarm
    glTranslatef(0,-rarm.sy,0)
    glRotatef(rfarm.rx,1,0,0)
    glTranslatef(0,-rfarm.sy,0)
    glPushMatrix() #start Scaling
    glScalef(rfarm.sx,rfarm.sy,rfarm.sz) 
    wall_mat = (rfarm.color[0],rfarm.color[1],rfarm.color[2],0)
    drawCube(wall_mat)
    glPopMatrix() #end Scaling
    glPopMatrix() #end rfarm
    glPopMatrix() #end right arm








def drawLegs():
    
    global luleg    #left legs
    glPushMatrix() #start luleg
    glTranslatef(-(0.4*trunk.sx),-trunk.sy,0)
    glRotatef(luleg.rx,1,0,0)
    glTranslatef(0,-luleg.sy,0)
    glPushMatrix() #start Scaling
    glScalef(luleg.sx,luleg.sy,luleg.sz)
    wall_mat = (luleg.color[0],luleg.color[1],luleg.color[2],0)
    drawCube(wall_mat)
    glPopMatrix() #end Scaling

    
    global llleg    #lfarm
    glPushMatrix() #start lfarm
    glTranslatef(0,-(luleg.sy),0)
    glRotatef(llleg.rx,1,0,0)
    glTranslatef(0,-llleg.sy,0)
    glPushMatrix() #start Scaling
    glScalef(llleg.sx,llleg.sy,llleg.sz) 
    wall_mat = (llleg.color[0],llleg.color[1],llleg.color[2],0)
    drawCube(wall_mat)
    glPopMatrix() #end Scaling
    glPopMatrix() #end llleg
    glPopMatrix() #end Left Leg

    
    global ruleg    #right Leg
    glPushMatrix() #start luleg
    glTranslatef(0.4*trunk.sx,-trunk.sy,0)
    glRotatef(ruleg.rx,1,0,0)
    glTranslatef(0,-ruleg.sy,0)
    glPushMatrix() #start Scaling
    glScalef(ruleg.sx,ruleg.sy,ruleg.sz)
    wall_mat = (ruleg.color[0],ruleg.color[1],ruleg.color[2],0)
    drawCube(wall_mat)
    glPopMatrix() #end Scaling

    
    global rlleg    #lfarm
    glPushMatrix() #start lfarm
    glTranslatef(0,-(ruleg.sy),0)
    glRotatef(rlleg.rx,1,0,0)
    glTranslatef(0,-rlleg.sy,0)
    glPushMatrix() #start Scaling
    glScalef(rlleg.sx,rlleg.sy,rlleg.sz) 
    wall_mat = (rlleg.color[0],rlleg.color[1],rlleg.color[2],0)
    drawCube(wall_mat)
    glPopMatrix() #end Scaling
    glPopMatrix() #end llleg
    glPopMatrix() #end Left Leg
    







def zoom(a):
    x = v.centerX - v.eyeX
    y = v.centerY - v.eyeY
    z = v.centerZ - v.eyeZ
    x_ = a*x
    y_ = a*y
    z_ = a*z
    e_ = (v.centerX - x_ , v.centerY - y_ , v.centerZ - z_)
    return View(e_[0],e_[1],e_[2],v.centerX,v.centerY,v.centerZ,v.upX,v.upY,v.upZ)

    
def load_texture(textureName):
    image = Image.open(textureName)
    imageData = image.tobytes("raw", "RGB", 0, -1)
    textureID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureID)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1],
                 0, GL_RGB, GL_UNSIGNED_BYTE, imageData)
    image.close()
    return textureID    
    



def myKey(key,x,y):
    global v
    #ROTATE
    if key == GLUT_KEY_F1:
        trunk.ry += 5
        trunk.ry %= 360
    if key == GLUT_KEY_F2:
        trunk.ry -= 5
        trunk.ry %= 360
    #zoom in zoom out 
    if key == GLUT_KEY_F3:
        v1 = zoom(0.80)
        v = v1
    if key == GLUT_KEY_F4:
        v1 = zoom(1.2)
        v = v1

    #camera
    if key == GLUT_KEY_LEFT:
        v.eyeX-=1.0
        v.centerX-=1.0
    if key == GLUT_KEY_RIGHT:
        v.eyeX+=1.0
        v.centerX+=1.0
    if key == GLUT_KEY_UP:
        v.eyeY+= 1.0
        v.centerY+=1.0
    if key == GLUT_KEY_DOWN:
        v.eyeY-= 1.0
        v.centerY-=1.0
    glutPostRedisplay()  #void glutPostRedisplay(void). Через glutReshapeFunc() устанавливается функция обработки изменения размеров окна пользователем, которой передаются новые размеры.


           

glutInit(sys.argv)#Выполним инициализацию OpenGl: glutInit(sys.argv)
glutInitWindowPosition(50,25)#ПОЗИЦИЯ ОКНА
glutInitWindowSize(500,500)#РАЗМЕР ОКНА
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE| GLUT_DEPTH)#Итак, предположим, вы хотите создать окно в цветовом пространстве RGB , с двойной буферизацией, с использованием буфера глубины. Все, что вам нужно сделать, это прописать соответствующие константы для того, чтобы создать необходимый режим.
glutCreateWindow("ROBOT")#ИМЯ ОКНА
glutReshapeFunc(resize)#РЕСАЙЗ
init()#ИНИЦИАЛИЗАЦИЯ
glutDisplayFunc(display)#Дисплей
glutSpecialFunc(myKey)#Клавиши
glutMainLoop()#Запуск