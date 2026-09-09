"""G-X plot adapted from Jordan Ando's interactive_GX_phase_diagrams notebook.

Retains the original least-squares common-tangent solver.
"""
import io
import itertools
import numpy as np
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
from scipy.optimize import least_squares


def obj_func(p, par1, par2):
     (x1, y1, x2, y2, m) = p

     eqn1 = np.polyval(par1, x1) - y1
     eqn2 = np.polyval(par2, x2) - y2
     eqn3 = 2*par1[0] * x1 + par1[1] - m
     eqn4 = 2*par2[0] * x2 + par2[1] - m
     eqn5 = m * (x1 - x2) - (y1 - y2)

     return [eqn1, eqn2, eqn3, eqn4, eqn5]

def convert_standard_to_lin(pstandard):
    [height, width, shift] = pstandard
    return[width, -2 * shift * width, shift **2 * width + height]

def plot_G_X_diagram(curves):

    [pstandard_1, pstandard_2, pstandard_3] = curves

    combs = list(itertools.combinations(curves, 2))

    par1 = convert_standard_to_lin(pstandard_1)
    par2 = convert_standard_to_lin(pstandard_2)
    par3 = convert_standard_to_lin(pstandard_3)


    plt.ylim(-15,15)

    xs = np.linspace(-5, 5, 1000)

    

    outs = []
    optimalities = []

    for (par_a, par_b) in combs:

        mid_a = par_a[2]
        mid_b = par_b[2]

        x0_1 = [mid_a - 4, 0, mid_b - 4, 0, -1]
        x0_2 = [mid_a + 4, 0, mid_b + 4, 0, 1]

        pa = convert_standard_to_lin(par_a)
        pb = convert_standard_to_lin(par_b)

        previous_x1 = []
        previous_xrange = []

        bounds = [((-np.inf, -np.inf, -np.inf, -np.inf, -np.inf), (np.inf, np.inf, np.inf, np.inf, 0)), ((-np.inf, -np.inf, -np.inf, -np.inf, 0), (np.inf, np.inf, np.inf, np.inf,np.inf))]


        for jdx, start_condition in enumerate([x0_1, x0_2]):


            output = least_squares(obj_func, x0 = start_condition, bounds = bounds[jdx], args = (pa, pb))
            opt = (output.optimality)
            out = output.x


            if opt > 1e-6:
                continue


            [x1, y1, x2, y2, m] = out


            lower_than_parab = True
            for parab in [par1, par2, par3]:
                if pa == parab or pb == parab:
                    continue

                else:
                    parab_vals = np.polyval(parab, np.linspace(np.min([x1,x2]), np.max([x1,x2]), 1000))
                    b = y1 - m * x1

                    if x1 > x2:
                        x_tan = np.linspace(x2, x1, 1000)
                    else:
                        x_tan = np.linspace(x1, x2, 1000)

                    tangent = x_tan * m + b

                    diff = parab_vals - tangent

                    if np.any(diff < 0):

                        lower_than_parab = False

            if not lower_than_parab:
                continue


            if np.abs(x2 - x1) < .001 or y2 > 200 or y1 > 2000 or np.abs(m) < np.abs(3e-16):
                continue

            is_lowest = True

            for idx, prev in enumerate(outs):
                if prev is None:
                    continue
                xl_prev= np.min([prev[0], prev[2]])
                xr_prev = np.max([prev[0], prev[2]])
                yl_prev = prev[prev.tolist().index(xl_prev) + 1]

                xl = np.min([out[0], out[2]])
                xr = np.max([out[0], out[2]])
                yl = out[out.tolist().index(xl) + 1]

                if not (np.max([xl_prev, xl]) <= np.min([xr_prev, xr])):
                    continue


                else:
                    """if np.abs(xl - xl_prev) <= 0.001:
                        continue"""
                

                    if xl < xl_prev:
                        yl_test = xl_prev * out[-1] + (yl - out[-1] * xl)
                        if yl_test < yl_prev:
                            outs[idx] = None
                        else:    
                            is_lowest = False
                    else:
                        yl_prev_test = x1 * prev[-1] + (yl_prev - prev[-1] * yl_prev)
                        if yl < yl_prev_test:
                            outs[idx] = None
                        else:    
                            is_lowest = False

                    """if yl < yl_prev:
                        outs[idx] = None
                    else:    
                        is_lowest = False"""
                    
            if is_lowest:
                outs.append(out)



    y1s = np.polyval(par1, xs)
    y2s = np.polyval(par2, xs)
    y3s = np.polyval(par3, xs)

    plt.plot(xs, y1s, '-', color= 'green')
    plt.plot(xs, y2s, '-', color = 'orange')
    plt.plot(xs, y3s, '-', color = 'purple')
    
    for out in outs:

        if out is None:
            continue
        [x1, y1, x2, y2, m] = out

        b = y1 - m * x1

        if x1 > x2:
            x_tan = np.linspace(x2, x1)
        else:
            x_tan = np.linspace(x1, x2)

        tangent = x_tan * m + b



        plt.plot(x_tan, tangent, color = "black")
        ylim = plt.gca().get_ylim()
        dylim = ylim[1]-ylim[0]
        plt.axvline(x1, ymax = 1+(y1 - ylim[1])/dylim, linestyle = '--')
        plt.axvline(x2, ymax = 1+(y2 - ylim[1])/dylim,linestyle = '--')
        plt.xlim(0, 1)
        plt.xlabel("X2")
        plt.ylabel("G")
    return plt.gcf()


def render_plot(parameters):
    """Return an SVG using the original notebook's three [height, width, shift] curves."""
    plt.close("all")
    fig, ax = plt.subplots(figsize=(7, 4.8), layout="constrained")
    try:
        plot_G_X_diagram(parameters)
        # Label and bound the axes even when no common tangent is found.
        ax.set_xlim(0, 1)
        ax.set_xlabel("X₂")
        ax.set_ylabel("G")
        ax.legend(ax.lines[:3], ["Phase 1", "Phase 2", "Phase 3"], loc="upper right")
        output = io.StringIO()
        fig.savefig(output, format="svg")
        return output.getvalue()
    finally:
        plt.close(fig)
