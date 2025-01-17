# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 15:44:04 2022

@author: PK
"""

import numpy as np

from light_prop.algorithms import GerchbergSaxton
from light_prop.calculations import get_gaussian_distribution
from light_prop.lightfield import LightField
from light_prop.propagation.params import PropagationParams
from light_prop.visualisation import GeneratePropagationPlot
from light_prop.calculations import gaussian

if __name__ == "__main__":
    params = PropagationParams.get_example_propagation_data()

    params.sigma = 4
    params.matrix_size = 256
    params.pixel = 0.9
    x_shift1 = 50
    x_shift2 = 25
    target = np.array(
        [[gaussian(np.sqrt((x - x_shift1) ** 2 + y ** 2), params.sigma) for x in
          np.arange(-params.matrix_size / 2, params.matrix_size / 2) * params.pixel] for y in
         np.arange(-params.matrix_size / 2, params.matrix_size / 2) * params.pixel]) + np.array(
        [[gaussian(np.sqrt((x - x_shift2) ** 2 + y ** 2), params.sigma) for x in
          np.arange(-params.matrix_size / 2, params.matrix_size / 2) * params.pixel] for y in
         np.arange(-params.matrix_size / 2, params.matrix_size / 2) * params.pixel])
    params.sigma = 50
    amp = get_gaussian_distribution(params)
    phase = np.array(
        [[0 for x in
          np.arange(-params.matrix_size / 2, params.matrix_size / 2) * params.pixel] for y in
         np.arange(-params.matrix_size / 2, params.matrix_size / 2) * params.pixel])

    GS = GerchbergSaxton(params)

    res = GS.optimize(LightField(amp, phase), LightField(target, phase), 5)

    plotter = GeneratePropagationPlot(res[0], output_type=GeneratePropagationPlot.PLOT_PHASE)
    plotter.save_output_as_figure("outs/structure.png")
    plotter.show()

    plotter = GeneratePropagationPlot(res[0], output_type=GeneratePropagationPlot.PLOT_ABS)
    plotter.save_output_as_figure("outs/input_field.png")
    
    plotter = GeneratePropagationPlot(res[1], output_type=GeneratePropagationPlot.PLOT_ABS)
    plotter.save_output_as_figure("outs/result.png")
    plotter.show()

    plotter = GeneratePropagationPlot(LightField(target, phase), output_type=GeneratePropagationPlot.PLOT_ABS)
    plotter.save_output_as_figure("outs/target.png")
    plotter.show()
