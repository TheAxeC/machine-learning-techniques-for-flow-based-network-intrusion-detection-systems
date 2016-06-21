import numpy as np

def plot_learning_curve(estimator, title, X, y, ylim=(0,1), cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5), save=True, baseline=True):
    """
    Generate a simple plot of the test and traning learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : integer, cross-validation generator, optional
        If an integer is passed, it is the number of folds (defaults to 3).
        Specific cross-validation objects can be passed, see
        sklearn.cross_validation module for the list of possible objects

    n_jobs : integer, optional
        Number of jobs to run in parallel (default 1).
    """
    import matplotlib.pyplot as plt
    from sklearn import cross_validation
    from sklearn.naive_bayes import GaussianNB
    from sklearn.svm import SVC
    from sklearn.datasets import load_digits
    from sklearn.learning_curve import learning_curve

    plt.figure()
    plt.title(title, fontsize=25)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples", fontsize=25)
    plt.ylabel("Accuracy", fontsize=25)
    
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    if baseline:
        from sklearn import dummy
        rand = dummy.DummyClassifier(strategy='uniform')
        train_sizes_rand, train_scores_rand, test_scores_rand = learning_curve(
            rand, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
        train_scores_mean_rand = np.mean(train_scores_rand, axis=1)
        train_scores_std_rand = np.std(train_scores_rand, axis=1)
        test_scores_mean_rand = np.mean(test_scores_rand, axis=1)
        test_scores_std_rand = np.std(test_scores_rand, axis=1)

        plt.fill_between(train_sizes_rand, train_scores_mean_rand - train_scores_std_rand,
                         train_scores_mean_rand + train_scores_std_rand, alpha=0.1,
                         color="b")
        plt.fill_between(train_sizes_rand, test_scores_mean_rand - test_scores_std_rand,
                         test_scores_mean_rand + test_scores_std_rand, alpha=0.1, color="c")
        plt.plot(train_sizes_rand, train_scores_mean_rand, 'o-', color="b",
                 label="Baseline Training score")
        plt.plot(train_sizes_rand, test_scores_mean_rand, 'o-', color="c",
                 label="Baseline Cross-validation score")

    #plt.legend(loc="best")
    if save:
        plt.savefig(title.replace(" ", "_"))
    return plt
