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
        self.file_name = None


    def generate_random_points(self, n_points):
        x = np.linspace(0, 76.2, 10)
        y = np.linspace(0, 76.2, 10)
        z = np.linspace(0, 76.2, 10)
        xx, yy, zz = np.meshgrid(x, y, z)
        points = np.column_stack([xx.ravel(), yy.ravel(), zz.ravel()])
        self.cloud = pv.PolyData(points)

    # def show_bounds(self):
    #     self.p.subplot(0, 1)
    #     self.shell_actor = self.p.show_bounds(grid='front', location='outer', ticks='both', show_xaxis=True,
    #                                           n_xlabels=5, n_ylabels=5, n_zlabels=5, xtitle='Length', ytitle='Width', ztitle='Height', axes_ranges=[0, 3000, 0, 3000, 0, 3000])

    def assign_data(self, data):
        self.cloud = pv.PolyData(data)
        self.cloud = self.cloud.clean()

    def delaunay_triangulation(self, alpha):
        global volume_calc
        volume = self.cloud.delaunay_3d(alpha=alpha)
        self.shell = volume.extract_geometry()
        volume_calc = self.shell.volume

    def create_plots(self):
        self.p = pv.Plotter(shape=(1, 2))  # create plotter screen

        # creating objects
        self.p.subplot(0, 0)  # left plot
        self.p.add_mesh(self.cloud, color='#f7cf60',
                        point_size=6)  # add the point cloud
        self.p.subplot(0, 1)  # right plot
        self.delaunay_triangulation(100)  # perform delaunay's triangulation
        self.shell_actor = self.p.add_mesh(
            self.shell, color='#f7cf60', show_edges=True, opacity=0.8, edge_color='#000000', line_width=2)  # add mesh to the plot

        # create text and buttons
        self.p.subplot(0, 1)  # right plot
        self.p.show_axes()
        self.p.add_slider_widget(self.edit_alpha, [
                                 0.001, 200], title='Alpha', n_steps=step, interaction_event='always', style="modern")  # alpha slider
        self.p.remove_actor(self.volume_actor)  # change out volume actor
        self.volume_actor = self.p.add_text(
            "Volume: " + str(round(volume_calc/16390, 3) * 2.54)+" cm cubed", position='upper_left', color='black', font_size=11)  # Add volume text

        self.p.add_checkbox_button_widget(
            self.set_fullscreen_right, value=False, color_on='white', color_off='black', background_color='gray')  # set right plot full screen
        self.p.add_text('Full Screen',
                        position=(70, 10), color='black', font_size=7)  # add text
        


        self.p.subplot(0, 0)  # left plot
        self.p.add_checkbox_button_widget(self.save_stl, value=False, color_on='gray', color_off='gray', background_color='gray',position=(10,140))  # save as stl
        self.p.add_text('Save as STL', position = (70,140), color='black', font_size=7)

        self.p.add_text('Full Screen',
                        position=(70, 10), color='black', font_size=7)  # add text
        self.p.add_checkbox_button_widget(
            self.set_fullscreen_left, value=False, color_on='white', color_off='black', background_color='gray')  # set left plot full screen

        self.p.add_text('Dark Mode',
                        position=(70, 75), color='black', font_size=7)
        self.p.add_checkbox_button_widget(self.color_mode, value=False, position=(
            10, 75), color_on='white', color_off='black', background_color='gray')
        self.color_mode(False)
        # self.p.show_axes_all()
        self.p.view_isometric()
        self.p.link_views()
        # self.show_bounds()

        self.p.show(full_screen=True)

    def color_mode(self, flag):
        if (flag):
            # self.p.set_background(color='#36393F')
            self.p.set_background(color='#44484f')
        else:
            self.p.set_background(color='#FFFFFF')

    def edit_alpha(self, value):
        self.p.subplot(0, 1)
        self.p.remove_actor(self.shell_actor)  # Remove the old mesh

        # Create the new mesh with the updated alpha value
        self.delaunay_triangulation(value)
        self.shell_actor = self.p.add_mesh(
            self.shell, color='#f7cf60', show_edges=True, opacity=0.8, edge_color='#000000', line_width=2)

        self.p.remove_actor(self.volume_actor)
        self.volume_actor = self.p.add_text(
            "Volume: " + str(round(volume_calc/16390, 3) * 2.54) + " cm cubed", position='upper_left', color='black', font_size=11)

        self.p.reset_camera()  # Reset the camera views to fit the new mesh

    def edit_alpha_fullscreen(self, value):
        self.p.remove_actor(self.shell_actor)  # Remove the old mesh

        # Create the new mesh with the updated alpha value
        self.delaunay_triangulation(value)
        self.shell_actor = self.p.add_mesh(
            self.shell, color='#f7cf60', show_edges=True, opacity=0.8, edge_color='#000000', line_width=2)

        self.p.remove_actor(self.volume_actor)
        self.volume_actor = self.p.add_text(
            "Volume: " + str(round(volume_calc/16390, 3)* 2.54) + " cm cubed", position='upper_right', color='black', font_size=11)

        # self.p.reset_camera()  # Reset the camera views to fit the new mesh

    def set_fullscreen_left(self, flag):
        start_position = 600
        vertical_alignment = 10

        if (flag):
            self.p.close(render=False)
            self.p = pv.Plotter()
            self.p.add_mesh(self.cloud, color='#f7cf60', point_size=6)
            self.p.view_isometric()
            self.p.add_text('Return',
                            position=(70, 10), color='black', font_size=7)  # add text

            self.p.add_checkbox_button_widget(self.set_fullscreen, value=False)
            self.p.add_text('Dark Mode',
                            position=(70, 75), color='black', font_size=7)
            self.p.add_checkbox_button_widget(self.color_mode, value=False, position=(
                10, 75), color_on='white', color_off='black', background_color='gray')
            self.p.show_axes_all()

            self.p.add_checkbox_button_widget(self.view_xy, value=False, position=(
                start_position, vertical_alignment), color_on='gray', color_off='gray', background_color='gray')
            self.p.add_text('XY',
                            position=(start_position, vertical_alignment + 50), color='black', font_size=7)

            self.p.add_checkbox_button_widget(self.view_xz, value=False, position=(
                start_position+60, vertical_alignment), color_on='gray', color_off='gray', background_color='gray')
            self.p.add_text('XZ',
                            position=(start_position+60, vertical_alignment + 50), color='black', font_size=7)

            self.p.add_checkbox_button_widget(self.view_yx, value=False, position=(
                start_position+120, vertical_alignment), color_on='gray', color_off='gray', background_color='gray')
            self.p.add_text('YX',
                            position=(start_position+120, vertical_alignment + 50), color='black', font_size=7)

            self.p.add_checkbox_button_widget(self.view_yz, value=False, position=(
                start_position+180, vertical_alignment), color_on='gray', color_off='gray', background_color='gray')
            self.p.add_text('YZ',
                            position=(start_position+180, vertical_alignment + 50), color='black', font_size=7)

            self.p.add_checkbox_button_widget(self.view_zx, value=False, position=(
                start_position+240, vertical_alignment), color_on='gray', color_off='gray', background_color='gray')
            self.p.add_text('ZX',
                            position=(start_position+240, vertical_alignment + 50), color='black', font_size=7)

            self.p.add_checkbox_button_widget(self.view_zy, value=False, position=(
                start_position+300, vertical_alignment), color_on='gray', color_off='gray', background_color='gray')
            self.p.add_text('ZY',
                            position=(start_position+300, vertical_alignment + 50), color='black', font_size=7)

            self.p.add_checkbox_button_widget(self.view_iso, value=False, position=(
                start_position+360, vertical_alignment), color_on='gray', color_off='gray', background_color='gray')
            self.p.add_text('ISO',
                            position=(start_position+360, vertical_alignment + 50), color='black', font_size=7)

            self.p.show(full_screen=True)
        else:
            self.create_plots()

    def set_fullscreen_right(self, flag):
        start_position = 600
        vertical_alignment = 10
        if (flag):
            self.p.close(render=False)
            self.p = pv.Plotter()
            self.shell_actor = self.p.add_mesh(
                self.shell, color='blue', show_edges=True)
            self.p.view_isometric()
            self.p.add_text('Return',
                            position=(70, 10), color='black', font_size=7)  # add text
            self.p.add_slider_widget(self.edit_alpha_fullscreen, [
                                     0.001, 200], title='Alpha', n_steps=step, interaction_event='always', style="modern")
            self.p.add_checkbox_button_widget(
                self.set_fullscreen, value=False,)
            self.p.add_text('Dark Mode',
                            position=(70, 75), color='black', font_size=7)
            self.p.add_checkbox_button_widget(self.color_mode, value=False, position=(
                10, 75), color_on='white', color_off='black', background_color='gray')


            self.p.add_checkbox_button_widget(self.view_xy, value=False, position=(
                start_position, vertical_alignment), color_on='gray', color_off='gray', background_color='gray')
            self.p.add_text('XY',
                            position=(start_position, vertical_alignment + 50), color='black', font_size=7)

            self.p.add_checkbox_button_widget(self.view_xz, value=False, position=(
                start_position+60, vertical_alignment), color_on='gray', color_off='gray', background_color='gray')
            self.p.add_text('XZ',
                            position=(start_position+60, vertical_alignment + 50), color='black', font_size=7)

            self.p.add_checkbox_button_widget(self.view_yx, value=False, position=(
                start_position+120, vertical_alignment), color_on='gray', color_off='gray', background_color='gray')
            self.p.add_text('YX',
                            position=(start_position+120, vertical_alignment + 50), color='black', font_size=7)

            self.p.add_checkbox_button_widget(self.view_yz, value=False, position=(
                start_position+180, vertical_alignment), color_on='gray', color_off='gray', background_color='gray')
            self.p.add_text('YZ',
                            position=(start_position+180, vertical_alignment + 50), color='black', font_size=7)

            self.p.add_checkbox_button_widget(self.view_zx, value=False, position=(
                start_position+240, vertical_alignment), color_on='gray', color_off='gray', background_color='gray')
            self.p.add_text('ZX',
                            position=(start_position+240, vertical_alignment + 50), color='black', font_size=7)

            self.p.add_checkbox_button_widget(self.view_zy, value=False, position=(
                start_position+300, vertical_alignment), color_on='gray', color_off='gray', background_color='gray')
            self.p.add_text('ZY',
                            position=(start_position+300, vertical_alignment + 50), color='black', font_size=7)

            self.p.add_checkbox_button_widget(self.view_iso, value=False, position=(
                start_position+360, vertical_alignment), color_on='gray', color_off='gray', background_color='gray')
            self.p.add_text('ISO',
                            position=(start_position+360, vertical_alignment + 50), color='black', font_size=7)
            
            self.p.show_axes_all()
            self.p.show(full_screen=True)

        else:
            self.create_plots()

    def set_fullscreen(self, flag):
        if (flag):
            self.p.close(render=False)
            self.create_plots()
        else:
            pass

    def view_xy(self, flag):
        self.p.view_xy()

    def view_xz(self, flag):
        self.p.view_xz()

    def view_yx(self, flag):
        self.p.view_yx()

    def view_yz(self, flag):
        self.p.view_yz()

    def view_zx(self, flag):
        self.p.view_zx()

    def view_zy(self, flag):
        self.p.view_zy()

    def view_iso(self, flag):
        self.p.view_isometric()

    def save_stl(self, flag):
        self.shell.save(self.file_name, recompute_normals=True)

def main():
    # run this program after the setup from control.py is completed
    pass
