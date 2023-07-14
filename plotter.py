import numpy as np
import pyvista as pv

range_start = 0.001
range_end = 200
n_steps = 10000

log_range_start = np.log10(range_start)
log_range_end = np.log10(range_end)
log_step = (log_range_end - log_range_start) / n_steps

step = 10 ** log_step

volume_calc = None

class plot_manager:
    def __init__(self):
        self.p = None
        self.data = None
        self.cloud = None
        self.shell = None
        self.alpha = 100
        self.shell_actor = None
        self.volume_actor = None

    def generate_random_points(self, n_points):
        # points = np.random.rand(n_points, 3) * 100
        # self.cloud = pv.PolyData(points)
        x = np.linspace(0, 76.2, 10)
        y = np.linspace(0, 76.2, 10)
        z = np.linspace(0, 76.2, 10)
        xx, yy, zz = np.meshgrid(x, y, z)
        points = np.column_stack([xx.ravel(), yy.ravel(), zz.ravel()])
        self.cloud = pv.PolyData(points)



    def assign_data(self, data):
        self.cloud = pv.PolyData(data)

    def delaunay_triangulation(self, alpha):
        global volume_calc
        volume = self.cloud.delaunay_3d(alpha=alpha)
        self.shell = volume.extract_geometry()
        volume_calc = self.shell.volume

    def create_plots(self):
        self.p = pv.Plotter(shape=(1, 2))
        # pv.Renderer
        self.p.subplot(0, 0)
        self.p.add_mesh(self.cloud, color='#f7cf60', point_size=6)
        self.p.subplot(0, 1)
        self.delaunay_triangulation(100)
        self.shell_actor = self.p.add_mesh(self.shell, color='#f7cf60', show_edges=True, opacity=0.8, edge_color='#000000', line_width=2)
        self.p.view_isometric()
        self.p.link_views()
        
        self.p.subplot(0, 1)
        self.p.add_slider_widget(self.edit_alpha, [0.001, 200], title='Alpha', n_steps = step, interaction_event = 'always', style="modern")
        self.p.remove_actor(self.volume_actor)
        self.volume_actor = self.p.add_text("Volume: "+ str(round(volume_calc/16390, 3))+" inches cubed", position='upper_left',color='black',font_size=11)

        self.p.add_checkbox_button_widget(self.set_fullscreen_right, value=False)

        self.p.subplot(0, 0)
        self.p.add_text('Click the Button in the bottom left to make the respective view full screen', position='upper_left',color='black',font_size=11)
        self.p.add_checkbox_button_widget(self.set_fullscreen_left, value=False)

        self.p.add_text('Click the next button up to toggle light/dark mode', position=(5,750),color='black',font_size=7)
        self.p.add_checkbox_button_widget(self.color_mode, value=False, position=(10,75), color_on='white', color_off='gray' )
        self.color_mode(False)
        self.p.show(full_screen=True)   

    def color_mode(self, flag):
        if(flag):
            self.p.set_background(color='#36393F')
        else: 
            self.p.set_background(color='#FFFFFF')


    def edit_alpha(self, value):
        self.p.subplot(0, 1)
        self.p.remove_actor(self.shell_actor)  # Remove the old mesh

        # Create the new mesh with the updated alpha value
        self.delaunay_triangulation(value)
        self.shell_actor = self.p.add_mesh(self.shell, color='#f7cf60', show_edges=True, opacity=0.8, edge_color='#000000', line_width=2)

        self.p.remove_actor(self.volume_actor)
        self.volume_actor = self.p.add_text("Volume: "+ str(round(volume_calc/16390, 3)) +" inches cubed", position='upper_left',color='black',font_size=11)

        self.p.reset_camera()  # Reset the camera views to fit the new mesh

    def edit_alpha_fullscreen(self, value):
        self.p.remove_actor(self.shell_actor)  # Remove the old mesh

        # Create the new mesh with the updated alpha value
        self.delaunay_triangulation(value)
        self.shell_actor = self.p.add_mesh(self.shell, color='#f7cf60', show_edges=True, opacity=0.8, edge_color='#000000', line_width=2)

        self.p.remove_actor(self.volume_actor)
        self.volume_actor = self.p.add_text("Volume: "+ str(round(volume_calc/16390, 3)) +" inches cubed", position='upper_right',color='black',font_size=11)


        self.p.reset_camera()  # Reset the camera views to fit the new mesh

    def set_fullscreen_left(self, flag):
        if(flag):
            self.p.close(render=False)
            self.p = pv.Plotter()
            self.p.add_mesh(self.cloud, color='#f7cf60', point_size=6)
            self.p.view_isometric()
            self.p.add_text('Click the Button in the bottom left to return', position='upper_left',color='black',font_size=7)
            self.p.add_checkbox_button_widget(self.set_fullscreen, value=False)
            self.p.add_text('Click the next button up to toggle light/dark mode', position=(5,750),color='black',font_size=7)
            self.p.add_checkbox_button_widget(self.color_mode, value=False, position=(10,75), color_on='white', color_off='gray' )
            self.p.show(full_screen=True)
        else:
            self.create_plots()

    def set_fullscreen_right(self, flag):
        if(flag):
            self.p.close(render=False)
            self.p = pv.Plotter()
            self.shell_actor = self.p.add_mesh(self.shell, color='blue', show_edges=True)
            self.p.view_isometric()
            self.p.add_text('Click the Button in the bottom left to return', position='upper_left',color='black',font_size=7)
            self.p.add_slider_widget(self.edit_alpha_fullscreen, [0.001, 200], title='Alpha', n_steps = step, interaction_event = 'always', style="modern")
            self.p.add_checkbox_button_widget(self.set_fullscreen, value=False,)
            self.p.add_text('Click the next button up to toggle light/dark mode', position=(5,750),color='black',font_size=7)
            self.p.add_checkbox_button_widget(self.color_mode, value=False, position=(10,75), color_on='white', color_off='gray' )
            self.p.show(full_screen=True)
        else:
            self.create_plots()

    def set_fullscreen(self, flag):
        if(flag):
            self.p.close(render=False)
            self.create_plots()
        else: pass

def main():
    #run this program after the setup from control.py is completed
    pass
