from __future__ import division
import numpy as np
from vispy.scene.canvas import SceneCanvas
from vispy import gloo
from vispy import app
from vispy.util.transforms import ortho, translate



                    
filename="C:\\Users\\George\\Desktop\\VisPy\\trial3_storm_XY.txt"
A=np.fromfile(filename,sep=" ")
A=A.reshape((len(A)/2,2))
#A=A/(np.max(A))*100
A=np.concatenate((A,np.zeros((A.shape[0],1))),1)

filename="C:\\Users\\George\\Desktop\\VisPy\\trial3_puff_XY.txt"
B=np.fromfile(filename,sep=" ")
B=B.reshape((len(B)/2,2))
B=np.concatenate((B,np.zeros((B.shape[0],1))),1)

B[:,2]=2 #setting z position.  Greater positive value means closer to viewer.
C=np.concatenate((A,B),0)

n=C.shape[0]
# Create vertices
data = np.zeros(n, [('a_position', np.float32, 3),
                    ('a_bg_color', np.float32, 4),
                    ('a_fg_color', np.float32, 4),
                    ('a_size', np.float32, 1)])
data['a_position'] =  C #0.45 * np.random.randn(n, 3)

#set colour here 
data['a_bg_color'] = np.ones((n,4)) #0, 1, 0,255 # #np.random.uniform(0.85, 1.00, (n, 4)) 
data['a_bg_color'][:A.shape[0],:]=np.array([1,0,0,255])
data['a_bg_color'][A.shape[0]:,:]=np.array([0,1,0,255])

data['a_fg_color'] = 0, 0, 0,10

#set size here
data['a_size'] = np.ones((1,n)) #np.random.uniform(5, 10, n)
data['a_size'][:A.shape[0]]=np.array([1])
data['a_size'][A.shape[0]:]=np.array([5])



u_linewidth = .1
u_antialias = 1.0
u_size = 1


vert = """
#version 120

// Uniforms
// ------------------------------------
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform float u_linewidth;
uniform float u_antialias;
uniform float u_size;

// Attributes
// ------------------------------------
attribute vec3  a_position;
attribute vec4  a_fg_color;
attribute vec4  a_bg_color;
attribute float a_size;

// Varyings
// ------------------------------------
varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;

void main (void) {
    v_size = a_size * u_size;
    v_linewidth = u_linewidth;
    v_antialias = u_antialias;
    v_fg_color  = a_fg_color;
    v_bg_color  = a_bg_color;
    gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
    gl_PointSize = v_size + 2*(v_linewidth + 1.5*v_antialias);
}
"""

frag = """
#version 120

// Constants
// ------------------------------------


// Varyings
// ------------------------------------
varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;

// Functions
// ------------------------------------

// ----------------
float disc(vec2 P, float size)
{
    float r = length((P.xy - vec2(0.5,0.5))*size);
    r -= v_size/2;
    return r;
}

// ----------------



// Main
// ------------------------------------
void main()
{
    float size = v_size +2*(v_linewidth + 1.5*v_antialias);
    float t = v_linewidth/2.0-v_antialias;

    float r = disc(gl_PointCoord, size);
    //float r = square(gl_PointCoord, size);
    // float r = ring(gl_PointCoord, size);
    // float r = arrow_right(gl_PointCoord, size);
    // float r = diamond(gl_PointCoord, size);
    // float r = cross(gl_PointCoord, size);
    // float r = clober(gl_PointCoord, size);
    // float r = hbar(gl_PointCoord, size);
    // float r = vbar(gl_PointCoord, size);


    float d = abs(r) - t;
    if( r > (v_linewidth/2.0+v_antialias))
    {
        discard;
    }
    else if( d < 0.0 )
    {
       gl_FragColor = v_fg_color;
    }
    else
    {
        float alpha = d/v_antialias;
        alpha = exp(-alpha*alpha);
        if (r > 0)
            gl_FragColor = vec4(v_fg_color.rgb, alpha*v_fg_color.a);
        else
            gl_FragColor = mix(v_bg_color, v_fg_color, alpha);
    }
}
"""


# ------------------------------------------------------------ Canvas class ---
class Canvas(SceneCanvas):

    def __init__(self):
        SceneCanvas.__init__(self, keys='interactive')
        self.size = 800, 800
        self.program = gloo.Program(vert, frag)
        self.view = np.eye(4, dtype=np.float32)
        self.model = np.eye(4, dtype=np.float32)
        self.projection = np.eye(4, dtype=np.float32)
        self.scale=np.max(A)
        #scale(self.view,.2)
        self.pos=np.array([np.max(A)/2,np.max(A)/2])
        translate(self.view, -np.max(A)/2, -np.max(A)/2, -1)
        #self.pos=np.array([0,0])

        self.program.bind(gloo.VertexBuffer(data))
        self.program['u_linewidth'] = u_linewidth
        self.program['u_antialias'] = u_antialias
        self.program['u_model'] = self.model
        self.program['u_view'] = self.view
        self.program['u_size'] = 1 #SIZE OF POINTS

    def on_initialize(self, event):
        gloo.set_state('translucent', clear_color='white')
    def on_draw(self, event):
        gloo.clear()
        self.program.draw('points')


    def on_key_press(self, event):
        if event.text == ' ':
            if self.timer.running:
                self.timer.stop()
            else:
                self.timer.start()

    def on_resize(self, event):
        width, height = event.size
        self.width=width
        self.height=height
        gloo.set_viewport(0, 0, width, height)
        self.projection = ortho(-self.scale/2, self.scale/2, -self.scale/2, self.scale/2, -1, 100) #perspective(1.0, width / float(height), 1.0, 10000000.0)
        self.program['u_projection'] = self.projection

    def on_mouse_wheel(self, event):
        #print(event.delta[1])
        oldscale=self.scale
        if event.delta[1]>0:
            self.scale /=event.delta[1]+1
        else:
            self.scale *= -event.delta[1]+1
        factor=self.scale/oldscale
        self.event=event
        self.projection = ortho(-self.scale/2, self.scale/2, -self.scale/2, self.scale/2, -1, 100) #perspective(1.0, width / float(height), 1.0, 10000000.0)
        self.program['u_projection'] = self.projection
        self.view = np.eye(4, dtype=np.float32)
        x,y=self.getEventCoordinates(event)
        print(factor)
        if factor<1:
            x-(x-self.pos[0])/factor
            y-(y-self.pos[1])/factor
        else:
            x=self.pos[0]-(x-self.pos[0])/factor
            y=self.pos[1]-(y-self.pos[1])/factor
        self.pos[0]=x
        self.pos[1]=y
        translate(self.view, -x, -y, -1)
        self.program['u_view'] = self.view
        self.getEventCoordinates(self.event)
        self.update()        
    
    def on_mouse_move(self, event):
        if not event.is_dragging:
            self.mouse_pos=self.getEventCoordinates(event)
            print(self.mouse_pos)
        
        if event.is_dragging:
            delta=np.array(event.pos)-np.array(event.last_event.pos)
            delta=delta.astype(np.float)
            delta[0]=float(-delta[0])*(self.scale/self.width)
            delta[1]=float(delta[1])*(self.scale/self.height)
            self.pos=self.pos+delta
            self.mouse_pos+=delta
            #pos=np.array(event.pos)
            #pos=pos*self.program['u_size']+
            
            
            self.view = np.eye(4, dtype=np.float32)
            translate(self.view, -self.pos[0], -self.pos[1], -1)
            self.program['u_view'] = self.view
            self.update()          
    def getEventCoordinates(self,event):
        pos=np.array(event.pos)/np.array([self.width,self.height])
        pos[1]=1-pos[1]
        pos=self.scale*(pos-np.array([.5,.5]))+self.pos
        return pos

if __name__ == '__main__':
    self = Canvas()
    self.show()
    #app.run()