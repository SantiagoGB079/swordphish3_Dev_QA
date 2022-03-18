import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, matthews_corrcoef)

from src.models import models_utils

FIGURE_SIZE = (8, 6)


def evaluate_ml_model(model, data, output_column, dataset_name, features_type, kde_plot=False, far_frr_plot=False,
                      save_plot=False, plot_path='reports/plots/model_performance_{}.png', save_both_plots=False):
    # Pre-processing data
    x_test, y_test = models_utils.input_output_split(data=data, output_column=output_column)
    x_test = models_utils.input_preprocessing(x=x_test, features_type=features_type)

    # Predict phishing score (1-> Phishing)
    if type(model).__name__ in ['Sequential', 'Functional']:
        y_pred_proba = model.predict(x_test).ravel()
    else:
        y_pred_proba = model.predict_proba(x_test)[:, 1]

    # Store prediction of the model
    y = np.append(y_test, y_pred_proba, axis=0)
    tam = len(y)
    y = np.reshape(y, [2, int(tam / 2)])
    y = y.T
    np.savetxt('reports/results.csv', y, delimiter=',')

    # Compute metrics from prediction.
    metrics = compute_metrics(y_true=y_test, y_pred_proba=y_pred_proba)

    # Plot predicted probability distribution
    model_name = pathlib.Path(plot_path).stem
    plot_title = 'Swordphish3 - Features: {} \n Test Data: {} \n Model: {}'.format(features_type,
                                                                                   dataset_name, model_name)

    # Plot model performance.
    if kde_plot or far_frr_plot:
        fig, ax = plt.subplots(figsize=FIGURE_SIZE)

    # Plot FAR, FRR and Accuracy.
    if far_frr_plot:
        plot_far_frr(metrics_df=metrics, plot_title=plot_title, ax=ax, save_plot=save_both_plots,
                     plot_path="{0}_{2}.{1}".format(*plot_path.split('.') + ['err']))
    # Plot prediction histogram.
    if kde_plot:
        plot_predictions_histogram(y_true=y_test, y_pred_proba=y_pred_proba, plot_title=plot_title, ax=ax,
                                   save_plot=save_both_plots,
                                   plot_path="{0}_{2}.{1}".format(*plot_path.split('.') + ['kde']))

    # Save plot.
    if (kde_plot or far_frr_plot) and save_plot:
        print('Model performance saved in {}'.format(plot_path))
        fig.savefig(plot_path, dpi=300, bbox_inches='tight')
        fig.show()
    return metrics


def compute_metrics(y_true, y_pred_proba):
    # Find metrics for different thresholds
    min_th = 0
    n_th_splits = 10
    metrics_list = []
    for threshold in range(min_th, n_th_splits + 1):
        threshold = threshold / n_th_splits
        temp_predicted_labels = (np.array(y_pred_proba) > threshold).astype('int')
        accuracy = accuracy_score(y_true, temp_predicted_labels)
        specificity = recall_score(y_true, temp_predicted_labels, pos_label=0)
        recall = recall_score(y_true, temp_predicted_labels)
        precision = precision_score(y_true, temp_predicted_labels, zero_division=1)
        f1 = f1_score(y_true=y_true, y_pred=temp_predicted_labels)
        matt = matthews_corrcoef(y_true, temp_predicted_labels)
        metrics_results = {'threshold': threshold,
                           'precision': precision,
                           'recall': recall,
                           'f1': f1,
                           'accuracy': accuracy,
                           'specificity': specificity,
                           'matthews': matt
                           }
        metrics_list.append(metrics_results)
    # Save metrics in dataframe.
    results_df = pd.DataFrame(metrics_list)
    # Calculate FAR and FRR
    results_df['frr'] = 1 - results_df.recall
    results_df['far'] = 1 - results_df.specificity
    return results_df


def plot_predictions_histogram(y_true, y_pred_proba, plot_title, ax=None, save_plot=False,
                               plot_path='reports/plots/test_distribution.png'):
    # Plot the figure.
    if ax is None:
        fig, ax = plt.Figure(figsize=FIGURE_SIZE)
        plt.hist(y_pred_proba[y_true == 0], label='Legitimate', bins=20, range=(0, 1), density=True, alpha=0.5,
                 color='steelblue', weights=np.ones_like(y_pred_proba[y_true == 0]) / len(y_pred_proba[y_true == 0]))
        plt.hist(y_pred_proba[y_true == 1], label='Phishing', bins=20, range=(0, 1), density=True, alpha=0.5,
                 color='darkred', weights=np.ones_like(y_pred_proba[y_true == 1]) / len(y_pred_proba[y_true == 1]))
        plt.grid()
        plt.title(plot_title)
        plt.xlabel('Probability Score')
        plt.legend(loc='upper center')
    else:
        # Verify if a twin axis is needed
        if all((not ax.lines, not ax.patches)):
            #
            ax2 = ax
        else:
            ax2 = ax.twinx()

        ax2.hist(y_pred_proba[y_true == 0], label='Legitimate', bins=20, range=(0, 1), density=True, alpha=0.5,
                 color='darkgrey')
        ax2.hist(y_pred_proba[y_true == 1], label='Phishing', bins=20, range=(0, 1), density=True, alpha=0.5,
                 color='brown')
        plt.grid()
        # plt.title(plot_title)
        ax2.set_ylabel('Density', fontweight='bold')
        ax2.set_xlabel('Probability Score', fontweight='bold')
        ax2.legend(loc='center right')

    if save_plot:
        kde_fig, kde_ax = plt.subplots(figsize=FIGURE_SIZE)
        kde_ax.hist(y_pred_proba[y_true == 0], label='Legitimate', bins=20, range=(0, 1), density=True, alpha=0.5,
                    color='darkgrey')
        kde_ax.hist(y_pred_proba[y_true == 1], label='Phishing', bins=20, range=(0, 1), density=True, alpha=0.5,
                    color='brown')
        kde_ax.minorticks_on()
        kde_ax.grid(True, axis='both', which='major')
        kde_ax.grid(True, axis='both', which='minor', alpha=0.2, linestyle='-')
        kde_ax.set_title(plot_title, fontweight='bold')
        kde_ax.set_ylabel('Density', fontweight='bold')
        kde_ax.set_xlabel('Probability Score', fontweight='bold')
        kde_ax.legend(loc='center right')
        kde_fig.savefig(plot_path, dpi=300, bbox_inches='tight')


def plot_far_frr(metrics_df, plot_title, ax=None, save_plot=False, plot_path='reports/plots/test_far_frr.png'):
    # Plot FAR and FRR
    # fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    # Verify if a twin axis is needed
    if all((not ax.lines, not ax.patches)):
        ax2 = ax
    else:
        ax2 = ax.twinx()

    metrics_df.plot(x='threshold', y=['frr', 'far', 'accuracy'], color=['deepskyblue', 'navy', 'darkorange'],
                    linewidth=0.8, label=['FRR', 'FAR', 'Accuracy'], grid=True, style=['-.', '-', '--'], ax=ax2)
    ax2.minorticks_on()
    ax2.grid(True, axis='both', which='major')
    ax2.grid(True, axis='both', which='minor', alpha=0.2, linestyle='-')
    ax2.set_title(plot_title, fontweight='bold')
    ax2.set_ylabel('FAR/FRR/Accuracy', fontweight='bold')
    ax2.set_xlabel('Threshold', fontweight='bold')
    plt.legend(loc='center left')
    if save_plot:
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
