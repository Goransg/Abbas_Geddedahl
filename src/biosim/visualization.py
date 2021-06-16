# -*- coding: utf-8 -*-
# This file based on example files from lecture J05 in INF200 june block of 2021
# By Hans Ekkehard Plesser
"""
:mod:`visualization.Graphics` provides graphics support for BioSim.

.. note::
   * This module requires the program ``ffmpeg`` or ``convert``
     available from `<https://ffmpeg.org>` and `<https://imagemagick.org>`.
   * You can also install ``ffmpeg`` using ``conda install ffmpeg``
   * You need to set the  :const:`_FFMPEG_BINARY` and :const:`_CONVERT_BINARY`
     constants below to the command required to invoke the programs
   * You need to set the :const:`_DEFAULT_FILEBASE` constant below to the
     directory and file-name start you want to use for the graphics output
     files.

"""

import os
import subprocess
import glob
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'

_DEFAULT_GRAPHICS_DIR = os.path.join('..', 'data')
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_IMG_FORMAT = 'png'
_DEFAULT_MOVIE_FORMAT = 'mp4'


class Graphics:
    """
    Provides graphics for BioSim.
    Deletes existing videos and images with the same image naming and format in the same directory.

    :param img_dir: directory for image files; no images if None
    :type img_dir: str
    :param img_name: beginning of name for image files
    :type img_name: str
    :param img_fmt: image file format suffix
    :type img_fmt: str
    """

    def __init__(self, hist_specs, img_dir=None, img_name=None, img_fmt=None):

        self._img_base = None
        if img_name is None:
            img_name = _DEFAULT_GRAPHICS_NAME

        if img_dir is None:
            img_dir = _DEFAULT_GRAPHICS_DIR

        if img_fmt is None:
            img_fmt = _DEFAULT_IMG_FORMAT

        elif img_dir is not None:
            if not os.path.isdir(img_dir):
                os.makedirs(img_dir)
            elif os.path.isdir(img_dir):
                self._img_base = os.path.join(img_dir, img_name)
                old_files = glob.glob(img_dir+'/*')
                for item in old_files:
                    if ((item[-(len('.' + img_fmt)):] == ('.' + img_fmt))
                        and item[:len(self._img_base)] == self._img_base)\
                            or (item[-len(self._img_base + '.mp4'):] == (self._img_base + '.mp4'))\
                            or (item[-len(self._img_base + '.gif'):] == (self._img_base + '.gif')):
                        os.remove(item)
            else:
                pass
        else:
            self._img_base = None

        self._img_fmt = img_fmt if img_fmt is not None else _DEFAULT_IMG_FORMAT

        self._img_ctr = 0
        self._img_step = 1
        self._limits_w = None
        self._limits_f = None
        self._limits_a = None
        if hist_specs is not None and hist_specs.__contains__('weight') \
                and hist_specs.__contains__('fitness') and hist_specs.__contains__('age'):
            n_points_w = int(round(hist_specs['weight']['max'] / hist_specs['weight']['delta'])) + 1
            self._limits_w = np.linspace(0, hist_specs['weight']['max'], num=n_points_w)
            self._ymax = 10

            n_points_f = int(
                round(hist_specs['fitness']['max'] / hist_specs['fitness']['delta'])) + 1
            self._limits_f = np.linspace(0, hist_specs['fitness']['max'], num=n_points_f)

            n_points_a = int(round(hist_specs['age']['max'] / hist_specs['age']['delta'])) + 1
            self._limits_a = np.linspace(0, hist_specs['age']['max'], num=n_points_a)
        # else:
        #     raise ValueError('Invalid hist_specs')

        self._fig = None
        self._gs = None
        self._map_ax_one = None
        self._map_ax_two = None
        self._img_axis_one = None
        self._img_axis_two = None
        self._mean_ax = None
        self._mean_fit_ax = None
        self._mean_fit_line = None
        self._mean_fit_line_2 = None
        self._mean_age_ax = None
        self._mean_age_line = None
        self._mean_age_line_2 = None
        self._mean_line = None
        self._mean_line_2 = None
        self._mean_line_3 = None
        self._geomap_axis = None
        self._geodesc_axis = None
        self._geomap_img_axis = None
        self._geodesc_img_axis = None
        self._count_ax = None
        self._txt = None
        self._template = None
        self._histw_ax = None
        self._histw_line = None
        self._histw_line_2 = None
        self._histf_ax = None
        self._histf_line = None
        self._histf_line_2 = None
        self._hista_ax = None
        self._hista_line = None
        self._hista_line_2 = None

    def update(self, step, sys_map_first, sys_map_second, all_animals, n_herbivores, n_carnivores,
               w_herbivores, w_carnivores, f_herbivores, f_carnivores, a_herbivores, a_carnivores):
        """
        Updates graphics and year count with current data and save to file if necessary.

        :param step: current time step
        :param sys_map_first: current system status of herbivores (2d array)
        :param sys_map_second: current system status of herbivores (2d array)
        :param all_animals: current number of animals
        :param n_herbivores: current number of herbivores
        :param n_carnivores: current number of carnivores
        :param w_herbivores: current weights of carnivores
        :param w_carnivores: current weights of herbivores
        :param f_herbivores: current fitness of carnivores
        :param f_carnivores: current fitness of herbivores
        :param a_herbivores: current fitness of carnivores
        :param a_carnivores: current fitness of herbivores
        """
        if self._limits_w is not None:
            self._update_system_map_one(sys_map_first)
            self._update_system_map_two(sys_map_second)
            self._update_mean_graph(step, all_animals, n_herbivores, n_carnivores)
            self._update_hist_w(w_herbivores, w_carnivores)
            self._update_hist_f(f_herbivores, f_carnivores)
            self._update_hist_a(a_herbivores, a_carnivores)
            self._fig.canvas.flush_events()

            self._txt.set_text(self._template.format(step))

        plt.pause(1e-20)

        self._save_graphics(step)

    def make_movie(self, movie_fmt=None):
        """
        Creates MPEG4 movie from visualization images saved.

        .. :note:
            Requires ffmpeg for MP4 and magick for GIF

        :param movie_fmt: str indicating the format of the movie

        The movie is stored as img_base + movie_fmt
        """

        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt is None:
            movie_fmt = _DEFAULT_MOVIE_FORMAT

        if movie_fmt == 'mp4':
            try:
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_MAGICK_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._img_base),
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

    def setup(self, final_step, img_step, geographic_map):
        """
        Prepare graphics.

        Call this before calling :meth:`update()` for the first time after
        the final time step has changed.

        :param final_step: last time step to be visualised (upper limit of x-axis)
        :param img_step: interval between saving image to file
        :param geographic_map: The map of the Island
        """

        self._img_step = img_step

        if self._fig is None:
            self._fig = plt.figure(figsize=(19, 10))
            self._gs = gridspec.GridSpec(ncols=36, nrows=36, figure=self._fig)

        if self._limits_w is not None:
            self._img_step = img_step

            if self._map_ax_one is None:
                self._map_ax_one = self._fig.add_subplot(self._gs[16:36, 10:24])
                self._map_ax_one.set_title('Herbivore distribution', fontsize=8)
                self._img_axis_one = None

            if self._map_ax_two is None:
                self._map_ax_two = self._fig.add_subplot(self._gs[16:36, 26:36])
                self._map_ax_two.set_title('Carnivore distribution', fontsize=8)
                self._img_axis_two = None

            if self._geomap_axis is None:
                self._geomap_axis = self._fig.add_subplot(self._gs[:12, 28:])
                self._geomap_axis.set_title('Island map', fontsize=8)
                self._geomap_img_axis = None

            if self._geodesc_axis is None:
                self._geodesc_axis = self._fig.add_subplot(self._gs[:8, 24])
                self._geodesc_img_axis = None

            if self._mean_ax is None:
                self._mean_ax = self._fig.add_subplot(self._gs[:10, :14])
                self._mean_ax.set_xlabel("            year", fontsize=8)
                self._mean_ax.set_ylabel("Count", fontsize=8)
                self._mean_ax.set_title("Animal count", fontsize=8)
                plt.setp(self._mean_ax.get_xticklabels(), fontsize=6)
                plt.setp(self._mean_ax.get_yticklabels(), fontsize=6)

            self._mean_ax.set_xlim(0, final_step + 1)

            if self._mean_line is None:
                mean_plot = self._mean_ax.plot(np.arange(0, final_step + 1),
                                               np.full(final_step + 1, np.nan),
                                               label='Overall population')
                self._mean_line = mean_plot[0]
            else:
                x_data, y_data = self._mean_line.get_data()
                x_new = np.arange(x_data[-1] + 1, final_step + 1)
                if len(x_new) > 0:
                    y_new = np.full(x_new.shape, np.nan)
                    self._mean_line.set_data(np.hstack((x_data, x_new)),
                                             np.hstack((y_data, y_new)))

            if self._mean_line_2 is None:
                mean_plot_2 = self._mean_ax.plot(np.arange(0, final_step + 1),
                                                 np.full(final_step + 1, np.nan),
                                                 c='g', label='Herbivores')
                self._mean_line_2 = mean_plot_2[0]
            else:
                x_data, y_data = self._mean_line_2.get_data()
                x_new = np.arange(x_data[-1] + 1, final_step + 1)
                if len(x_new) > 0:
                    y_new = np.full(x_new.shape, np.nan)
                    self._mean_line_2.set_data(np.hstack((x_data, x_new)),
                                               np.hstack((y_data, y_new)))

            if self._mean_line_3 is None:
                mean_plot_3 = self._mean_ax.plot(np.arange(0, final_step + 1),
                                                 np.full(final_step + 1, np.nan),
                                                 c='r', label='Carnivores')
                self._mean_line_3 = mean_plot_3[0]
                self._mean_ax.legend(prop={'size': 6})
            else:
                x_data, y_data = self._mean_line_3.get_data()
                x_new = np.arange(x_data[-1] + 1, final_step + 1)
                if len(x_new) > 0:
                    y_new = np.full(x_new.shape, np.nan)
                    self._mean_line_3.set_data(np.hstack((x_data, x_new)),
                                               np.hstack((y_data, y_new)))

            if self._histw_ax is None:
                self._histw_ax = self._fig.add_subplot(self._gs[12:18, :8])
                self._histw_ax.set_xlabel("weight", fontsize=6)
                self._histw_ax.set_ylabel("Count", fontsize=6)
                self._histw_ax.set_title("Animal weights", fontsize=8)
                self._histw_line = self._histw_ax.step(self._limits_w[:-1],
                                                       np.zeros_like(self._limits_w[:-1]),
                                                       where='mid', lw=2, label='Herbivores')[0]
                self._histw_line_2 = self._histw_ax.step(self._limits_w[:-1],
                                                         np.zeros_like(self._limits_w[:-1]),
                                                         where='mid', lw=2, label='Carnivores')[0]
                self._histw_ax.set_xlim(self._limits_w[0], self._limits_w[-1])
                self._histw_ax.set_ylim(0, self._ymax)
                self._histw_ax.legend(prop={'size': 6})
                plt.setp(self._histw_ax.get_xticklabels(), fontsize=6)
                plt.setp(self._histw_ax.get_yticklabels(), fontsize=6)

            if self._histf_ax is None:
                self._histf_ax = self._fig.add_subplot(self._gs[21:27, :8])
                self._histf_ax.set_xlabel("fitness", fontsize=6)
                self._histf_ax.set_ylabel("Count", fontsize=6)
                self._histf_ax.set_title("Animal fitness", fontsize=8)
                self._histf_line = self._histf_ax.step(self._limits_f[:-1],
                                                       np.zeros_like(self._limits_f[:-1]),
                                                       where='mid', lw=2, label='Herbivores')[0]
                self._histf_line_2 = self._histf_ax.step(self._limits_f[:-1],
                                                         np.zeros_like(self._limits_f[:-1]),
                                                         where='mid', lw=2, label='Carnivores')[0]
                self._histf_ax.set_xlim(self._limits_f[0], self._limits_f[-1])
                self._histf_ax.set_ylim(0, self._ymax)
                self._histf_ax.legend(prop={'size': 6})
                plt.setp(self._histf_ax.get_xticklabels(), fontsize=6)
                plt.setp(self._histf_ax.get_yticklabels(), fontsize=6)

            if self._hista_ax is None:
                self._hista_ax = self._fig.add_subplot(self._gs[30:36, :8])
                self._hista_ax.set_xlabel("age", fontsize=6)
                self._hista_ax.set_ylabel("Count", fontsize=6)
                self._hista_ax.set_title("Animal age", fontsize=8)
                self._hista_line = self._hista_ax.step(self._limits_a[:-1],
                                                       np.zeros_like(self._limits_a[:-1]),
                                                       where='mid', lw=2, label='Herbivores')[0]
                self._hista_line_2 = self._hista_ax.step(self._limits_a[:-1],
                                                         np.zeros_like(self._limits_a[:-1]),
                                                         where='mid', lw=2, label='Carnivores')[0]
                self._hista_ax.set_xlim(self._limits_a[0], self._limits_a[-1])
                self._hista_ax.set_ylim(0, self._ymax)
                self._hista_ax.legend(prop={'size': 6})
                plt.setp(self._hista_ax.get_xticklabels(), fontsize=6)
                plt.setp(self._hista_ax.get_yticklabels(), fontsize=6)

            if self._count_ax is None:
                self._count_ax = self._fig.add_axes([0.4, 0.8, 0.2, 0.2])
                self._count_ax.axis('off')

            if self._template is None:
                self._template = 'Year: {:5d}'
                self._txt = self._count_ax.text(0.5, 0.5, self._template.format(0),
                                                horizontalalignment='center',
                                                verticalalignment='center',
                                                transform=self._count_ax.transAxes)

            self._init_geography(geographic_map)

    def _update_system_map_one(self, sys_map):
        """
        Update the 2D-view of the system for herbivore distribution.

        :param sys_map: A nested list indicating the distribution of herbivores
        """

        if self._img_axis_one is not None:
            self._img_axis_one.set_data(sys_map)
        else:
            self._img_axis_one = self._map_ax_one.imshow(sys_map,
                                                         interpolation='nearest',
                                                         vmin=0, vmax=200)

            plt.colorbar(self._img_axis_one, ax=self._map_ax_one,
                         orientation='horizontal', shrink=0.5)

    def _update_system_map_two(self, sys_map):
        """
        Update the 2D-view of the system for carnivore distribution.

        :param sys_map: A nested list indicating the distribution of carnivores
        """

        if self._img_axis_two is not None:
            self._img_axis_two.set_data(sys_map)
        else:
            self._img_axis_two = self._map_ax_two.imshow(sys_map,
                                                         interpolation='nearest',
                                                         vmin=0, vmax=50)

            plt.colorbar(self._img_axis_two, ax=self._map_ax_two,
                         orientation='horizontal', shrink=0.75)

    def _update_mean_graph(self, step, all_animals, n_herbivores, n_carnivores):
        """
        Updates the graph of animal populations

        :param step: INT the current year of simulation
        :param all_animals: INT the current amount of animals on the island
        :param n_herbivores: INT the current amount of herbivores on the island
        :param n_carnivores: INT the current amount of carnivores on the island
        """

        y_data = self._mean_line.get_ydata()
        y_data[step] = all_animals
        self._mean_line.set_ydata(y_data)
        self._mean_ax.set_ylim(0, max(y_data) + 1000)

        y_data_2 = self._mean_line_2.get_ydata()
        y_data_2[step] = n_herbivores
        self._mean_line_2.set_ydata(y_data_2)

        y_data_3 = self._mean_line_3.get_ydata()
        y_data_3[step] = n_carnivores
        self._mean_line_3.set_ydata(y_data_3)

    def _update_hist_w(self, w_herbivores, w_carnivores):
        """
        Updates the histograms of animal weight distribution

        :param w_herbivores: Nested Array containing the current weights of herbivores on the island
        :param w_carnivores: Nested Array containing the current weights of carnivores on the island
        """

        countswh = np.histogram(np.hstack(w_herbivores), self._limits_w)[0]
        self._histw_line.set_ydata(countswh)
        countswc = np.histogram(np.hstack(w_carnivores), self._limits_w)[0]
        self._histw_line_2.set_ydata(countswc)
        self._ymax = max(self._ymax, 1.05 * max(countswh))
        self._histw_ax.set_ylim(0, self._ymax)

    def _update_hist_f(self, f_herbivores, f_carnivores):
        """
        Updates the histograms of animal weight distribution

        :param f_herbivores: Nested Array containing the current fitness of herbivores on the island
        :param f_carnivores: Nested Array containing the current fitness of carnivores on the island
        """
        countsfh = np.histogram(np.hstack(f_herbivores), self._limits_f)[0]
        self._histf_line.set_ydata(countsfh)
        countsfc = np.histogram(np.hstack(f_carnivores), self._limits_f)[0]
        self._histf_line_2.set_ydata(countsfc)
        self._ymax = max(self._ymax, 1.05 * max(countsfh))
        self._histf_ax.set_ylim(0, self._ymax)

    def _update_hist_a(self, a_herbivores, a_carnivores):
        """
        Updates the histograms of animal weight distribution

        :param a_herbivores: Nested Array containing the current age of herbivores on the island
        :param a_carnivores: Nested Array containing the current age of carnivores on the island
        """

        countsah = np.histogram(np.hstack(a_herbivores), self._limits_a)[0]
        self._hista_line.set_ydata(countsah)
        countsac = np.histogram(np.hstack(a_carnivores), self._limits_a)[0]
        self._hista_line_2.set_ydata(countsac)
        self._ymax = max(self._ymax, 1.05 * max(countsah))
        self._hista_ax.set_ylim(0, self._ymax)

    def _save_graphics(self, step):
        """
        Saves graphics to file if file name given.

        :param step: the current year of simulation
        """

        if (self._img_base is None) or (self._img_step is None) or (step % self._img_step != 0):
            return None

        else:
            self._fig.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                               num=self._img_ctr,
                                                               type=self._img_fmt))
            self._img_ctr += 1

    def _init_geography(self, island_map):
        """
        Plots a geographical map of the island.

        :param island_map: A text string indicating the layout of the island.
        """

        if self._geomap_img_axis is not None:
            pass
        else:
            rgb_value = {'W': (0.0, 0.0, 1.0),
                         'L': (0.0, 0.6, 0.0),
                         'H': (0.5, 1.0, 0.5),
                         'D': (1.0, 1.0, 0.5)}

            map_rgb = [[rgb_value[column] for column in row]
                       for row in island_map.split()]

            self._geomap_axis.set_xticks(range(0, len(map_rgb[0]), 4))
            self._geomap_axis.set_xticklabels(range(1, 1 + len(map_rgb[0]), 4))
            self._geomap_axis.set_yticks(range(0, len(map_rgb), 4))
            self._geomap_axis.set_yticklabels(range(1, 1 + len(map_rgb), 4))
            self._geomap_img_axis = self._geomap_axis.imshow(map_rgb)

            for ix, name in enumerate(('Water', 'Lowland',
                                       'Highland', 'Desert')):
                self._geodesc_axis.axis('off')
                self._geodesc_axis.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                                           edgecolor='none',
                                                           facecolor=rgb_value[name[0]]))
                self._geodesc_axis.text(0.35, ix * 0.2, name,
                                        transform=self._geodesc_axis.transAxes)
