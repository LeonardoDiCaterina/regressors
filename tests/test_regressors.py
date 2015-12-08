#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_regressors
---------------

Tests for the `regressors` module.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np
import pandas as pd
import unittest2 as unittest
from sklearn import datasets
from sklearn import decomposition
from sklearn import linear_model
from sklearn import preprocessing

from regressors import regressors
from regressors import plots
from regressors import stats

boston = datasets.load_boston()
which_betas = np.ones(13, dtype=bool)
which_betas[3] = False  # Eliminate dummy variable
X = boston.data[:, which_betas]
y = boston.target


class TestLinearRegression(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_LinearRegression_fit_with_no_xlabels(self):
        ols = regressors.LinearRegression()
        try:
            ols.fit(X, y)
        except Exception as e:
            self.fail("Fitting with no xlabels raised unexpected "
                      "exception: {0}".format(e))

    def test_LinearRegression_fit_with_xlabels_as_args(self):
        ols = regressors.LinearRegression()
        labels = ['LABEL{0}'.format(i) for i in range(X.shape[1])]
        try:
            ols.fit(X, y, labels)
        except Exception as e:
            self.fail("Fitting with xlabels as *args raised unexpected "
                      "exception: {0}".format(e))

    def test_LinearRegression_fit_with_xlabels_as_kwargs(self):
        ols = regressors.LinearRegression()
        labels = ['LABEL{0}'.format(i) for i in range(X.shape[1])]
        try:
            ols.fit(X, y=y, xlabels=labels)
        except Exception as e:
            self.fail("Fitting with xlabels as **kwargs raised unexpected "
                      "exception: {0}".format(e))

    def test_LinearRegression_fit_with_xlabels_mixed_kwarg(self):
        ols = regressors.LinearRegression()
        labels = ['LABEL{0}'.format(i) for i in range(X.shape[1])]
        try:
            ols.fit(X, y, xlabels=labels)
        except Exception as e:
            self.fail("Fitting with xlabels as **kwargs with y also as "
                      "**kwargs raised unexpected exception: {0}".format(e))

    def test_LinearRegression_fit_with_xlabels_all_kwargs(self):
        ols = regressors.LinearRegression()
        labels = ['LABEL{0}'.format(i) for i in range(X.shape[1])]
        try:
            ols.fit(X=X, y=y, xlabels=labels)
        except Exception as e:
            self.fail("Fitting with xlabels with all parameters as "
                      "**kwargs raised unexpected exception: {0}".format(e))

    def test_LinearRegression_fit_with_xlabels_out_of_position_kwargs(self):
        ols = regressors.LinearRegression()
        labels = ['LABEL{0}'.format(i) for i in range(X.shape[1])]
        try:
            ols.fit(X=X, xlabels=labels, y=y)
        except Exception as e:
            self.fail("Fitting with xlabels with all parameters as "
                      "**kwargs raised unexpected exception: {0}".format(e))

    def test_LinearRegression_fit_with_xlabels_args_out_of_pos_args_fails(self):
        ols = regressors.LinearRegression()
        labels = ['LABEL{0}'.format(i) for i in range(X.shape[1])]
        with self.assertRaises(AssertionError):
            ols.fit(X, labels, y)

    def test_LinearRegression_xlabel_dimensions_error_checking(self):
        ols = regressors.LinearRegression()
        with self.assertRaises(AssertionError):
            ols.fit(X, y, xlabels=['LABEL1', 'LABEL2'])

    def test_LinearRegression_summary(self):
        ols = regressors.LinearRegression()
        labels = ['LABEL{0}'.format(i) for i in range(X.shape[1])]
        ols.fit(X, y, labels)
        summary = ols.summary()
        self.assertIsInstance(summary, pd.core.frame.DataFrame)
        try:
            str(summary)
        except Exception as e:
            self.fail("str(summary) raised "
                      "exception unexpectedly: {0}".format(e))


class TestStatsResiduals(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_classifier_type_assertion_raised(self):
        # Test that assertion is raised for unsupported model
        pcomp = decomposition.PCA()
        pcomp.fit(X, y)
        with self.assertRaises(AttributeError):
            stats.residuals(pcomp, X, y)

    def tests_classifier_type_assertion_not_raised(self):
        # Test that assertion is not raise for supported models
        for classifier in regressors.supported_linear_models:
            clf = classifier()
            clf.fit(X, y)
            try:
                stats.residuals(clf, X, y)
            except Exception as e:
                self.fail("Testing supported linear models in residuals "
                          "function failed unexpectedly: {0}".format(e))

    def test_getting_raw_residuals(self):
        ols = regressors.LinearRegression()
        ols.fit(X, y)
        try:
            stats.residuals(ols, X, y, r_type='raw')
        except Exception as e:
            self.fail("Testing raw residuals failed unexpectedly: "
                      "{0}".format(e))

    def test_getting_standardized_residuals(self):
        ols = regressors.LinearRegression()
        ols.fit(X, y)
        try:
            stats.residuals(ols, X, y, r_type='standardized')
        except Exception as e:
            self.fail("Testing standardized residuals failed unexpectedly: "
                      "{0}".format(e))

    def test_getting_studentized_residuals(self):
        ols = regressors.LinearRegression()
        ols.fit(X, y)
        try:
            stats.residuals(ols, X, y, r_type='studentized')
        except Exception as e:
            self.fail("Testing studentized residuals failed unexpectedly: "
                      "{0}".format(e))


class TestSummaryStats(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_error_not_raised_by_sse(self):
        # Test that assertion is not raise for supported models
        for classifier in regressors.supported_linear_models:
            clf = classifier()
            clf.fit(X, y)
            try:
                sse = stats.sse(clf, X, y)
            except Exception as e:
                self.fail("Testing SSE function for supported linear models "
                          "failed unexpectedly: {0}".format(e))

    def test_error_not_raised_by_adj_r2_score(self):
        # Test that assertion is not raise for supported models
        for classifier in regressors.supported_linear_models:
            clf = classifier()
            clf.fit(X, y)
            try:
                stats.adj_r2_score(clf, X, y)
            except Exception as e:
                self.fail("Testing adjusted R2 function for supported linear "
                          "models failed unexpectedly: {0}".format(e))

    def test_verify_adj_r2_score_return_type(self):
        for classifier in regressors.supported_linear_models:
            clf = classifier()
            clf.fit(X, y)
            adj_r2_score = stats.adj_r2_score(clf, X, y)
            self.assertIsInstance(adj_r2_score, float)

    def test_error_not_raised_by_coef_se(self):
        # Test that assertion is not raise for supported models
        for classifier in regressors.supported_linear_models:
            clf = classifier()
            clf.fit(X, y)
            try:
                stats.coef_se(clf, X, y).shape
            except Exception as e:
                self.fail("Testing standard error of coefficients function for "
                          "supported linear models failed "
                          "unexpectedly: {0}".format(e))

    def test_length_of_returned_coef_se(self):
        for classifier in regressors.supported_linear_models:
            clf = classifier()
            clf.fit(X, y)
            coef_se = stats.coef_se(clf, X, y)
            expected_length = X.shape[1] + 1  # Add 1 for the intercept
            self.assertEqual(coef_se.shape[0], expected_length)

    def test_error_not_raised_by_coef_tval(self):
        # Test that assertion is not raise for supported models
        for classifier in regressors.supported_linear_models:
            clf = classifier()
            clf.fit(X, y)
            try:
                stats.coef_tval(clf, X, y).shape
            except Exception as e:
                self.fail("Testing t-values of coefficients function for "
                          "supported linear models failed "
                          "unexpectedly: {0}".format(e))

    def test_length_of_returned_coef_tval(self):
        for classifier in regressors.supported_linear_models:
            clf = classifier()
            clf.fit(X, y)
            coef_tval = stats.coef_tval(clf, X, y)
            expected_length = X.shape[1] + 1  # Add 1 for the intercept
            self.assertEqual(coef_tval.shape[0], expected_length)

    def test_error_not_raised_by_coef_pval(self):
        # Test that assertion is not raise for supported models
        for classifier in regressors.supported_linear_models:
            clf = classifier()
            clf.fit(X, y)
            try:
                stats.coef_pval(clf, X, y).shape
            except Exception as e:
                self.fail("Testing p-values of coefficients function for "
                          "supported linear models failed "
                          "unexpectedly: {0}".format(e))

    def test_length_of_returned_coef_pval(self):
        for classifier in regressors.supported_linear_models:
            clf = classifier()
            clf.fit(X, y)
            coef_pval = stats.coef_tval(clf, X, y)
            expected_length = X.shape[1] + 1  # Add 1 for the intercept
            self.assertEqual(coef_pval.shape[0], expected_length)

    def test_error_not_raised_by_f_stat(self):
        # Test that assertion is not raise for supported models
        for classifier in regressors.supported_linear_models:
            clf = classifier()
            clf.fit(X, y)
            try:
                stats.f_stat(clf, X, y).shape
            except Exception as e:
                self.fail("Testing summary F-statistic function for "
                          "supported linear models failed "
                          "unexpectedly: {0}".format(e))

    def test_verify_f_stat_return_type(self):
        for classifier in regressors.supported_linear_models:
            clf = classifier()
            clf.fit(X, y)
            adj_r2_score = stats.adj_r2_score(clf, X, y)
            self.assertIsInstance(adj_r2_score, float)

    def test_error_not_raised_by_summary_function(self):
        for classifier in regressors.supported_linear_models:
            clf = classifier()
            clf.fit(X, y)
            try:
                stats.f_stat(clf, X, y).shape
            except Exception as e:
                self.fail("Testing summary function for "
                          "supported linear models failed "
                          "unexpectedly: {0}".format(e))


class TestPCRBetaCoef(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pcr_beta_coef_returns_coefs_for_all_predictors(self):
        # Just return the coefficients for the predictors because the intercept
        # for PCR is the same as the intercept in the PCA regression model.
        scaler = preprocessing.StandardScaler()
        x_scaled = scaler.fit_transform(X)
        pcomp = decomposition.PCA()
        pcomp.fit(x_scaled)
        x_reduced = pcomp.transform(x_scaled)
        ols = linear_model.LinearRegression()
        ols.fit(x_reduced, y)
        beta_coef = stats.pcr_beta_coef(ols, pcomp)
        self.assertEqual(beta_coef.shape, ols.coef_.shape)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
