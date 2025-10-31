"""
PMM2 для ARIMA моделей - ВИПРАВЛЕНА ВЕРСІЯ
===========================================

Ця версія базується на правильних формулах з R пакету EstemPMM
та теорії Кунченко-Заболотнія.

Автор: На основі робіт Zabolotnii S., Warsza Z.L., Kunchenko Y.P.
Дата: Жовтень 2025
"""

import numpy as np
from scipy import stats, optimize
from scipy.linalg import solve
from typing import Tuple, Dict, Optional
import warnings

warnings.filterwarnings('ignore')


def compute_moments(residuals: np.ndarray) -> Dict[str, float]:
    """
    Обчислення центральних моментів та кумулянтних коефіцієнтів.
    
    Parameters:
    -----------
    residuals : array-like
        Вектор залишків/інновацій
    
    Returns:
    --------
    moments : dict
        Словник з моментами (m2, m3, m4) та кумулянтними коефіцієнтами
    """
    residuals = np.asarray(residuals)
    residuals = residuals - np.mean(residuals)  # Центрування
    
    m2 = np.mean(residuals**2)
    m3 = np.mean(residuals**3)
    m4 = np.mean(residuals**4)
    
    # Кумулянти
    kappa2 = m2
    kappa3 = m3
    kappa4 = m4 - 3*m2**2
    
    # Кумулянтні коефіцієнти
    gamma3 = kappa3 / (kappa2**(3/2)) if kappa2 > 0 else 0
    gamma4 = kappa4 / (kappa2**2) if kappa2 > 0 else 0
    
    return {
        'm2': m2, 'm3': m3, 'm4': m4,
        'kappa2': kappa2, 'kappa3': kappa3, 'kappa4': kappa4,
        'gamma3': gamma3, 'gamma4': gamma4
    }


def fit_ar_pmm2_corrected(x: np.ndarray, p: int, include_mean: bool = True,
                          max_iter: int = 50, tol: float = 1e-6,
                          regularize: bool = True, reg_lambda: float = 1e-8,
                          verbose: bool = False) -> Dict:
    """
    Оцінювання AR(p) моделі методом PMM2 - ВИПРАВЛЕНА ВЕРСІЯ.
    
    Використовує ПРАВИЛЬНІ формули з R пакету EstemPMM:
    Z_j(β) = Σ x_{ij} [A*y_pred^2 + B*y_pred + C] = 0
    
    де:
    A = m3
    B = m4 - m2^2 - 2*m3*y
    C = m3*y^2 - (m4 - m2^2)*y - m2*m3
    
    Parameters:
    -----------
    x : array-like
        Часовий ряд
    p : int
        Порядок AR моделі
    include_mean : bool
        Включити константу
    max_iter : int
        Максимальна кількість ітерацій
    tol : float
        Точність збіжності
    regularize : bool
        Додавати регуляризацію до Якобіану
    reg_lambda : float
        Параметр регуляризації
    verbose : bool
        Виводити інформацію про прогрес
    
    Returns:
    --------
    results : dict
        Словник з результатами оцінювання
    """
    x = np.asarray(x)
    n = len(x)
    
    # Крок 1: Центрування даних
    if include_mean:
        x_mean = np.mean(x)
        x_centered = x - x_mean
    else:
        x_mean = 0
        x_centered = x
    
    # Крок 2: Формування матриці дизайну для AR(p)
    X_design = np.zeros((n - p, p))
    for i in range(p):
        X_design[:, i] = x_centered[p-i-1:n-i-1]
    
    y = x_centered[p:]
    
    # Крок 3: OLS оцінка для ініціалізації
    phi_ols = np.linalg.lstsq(X_design, y, rcond=None)[0]
    residuals_ols = y - X_design @ phi_ols
    
    # Крок 4: Обчислення моментів залишків
    moments = compute_moments(residuals_ols)
    m2, m3, m4 = moments['m2'], moments['m3'], moments['m4']
    gamma3, gamma4 = moments['gamma3'], moments['gamma4']
    
    if verbose:
        print(f"OLS залишки: γ₃ = {gamma3:.4f}, γ₄ = {gamma4:.4f}")
    
    # Крок 5: Перевірка асиметрії
    if abs(gamma3) < 0.1:
        if verbose:
            print("Warning: Низька асиметрія. PMM2 може не дати значної переваги.")
        return {
            'coefficients_ols': phi_ols,
            'coefficients_pmm2': phi_ols,
            'residuals_ols': residuals_ols,
            'residuals_pmm2': residuals_ols,
            'variance_ols': np.var(residuals_ols, ddof=p),
            'variance_pmm2': np.var(residuals_ols, ddof=p),
            'moments': moments,
            'variance_reduction': 0.0,
            'converged': True,
            'iterations': 0,
            'intercept': x_mean
        }
    
    # Крок 6: PMM2 ітеративна процедура (Ньютон-Рафсон)
    # Використовуємо формули з R пакету EstemPMM
    
    phi_pmm2 = phi_ols.copy()  # Початкове наближення
    converged = False
    
    for iteration in range(max_iter):
        # Передбачені значення
        y_pred = X_design @ phi_pmm2
        
        # Коефіцієнти PMM2 поліному (формули з R пакету)
        A = m3
        B = m4 - m2**2 - 2*m3*y
        C = m3*y**2 - (m4 - m2**2)*y - m2*m3
        
        # Z1 = A*y_pred^2 + B*y_pred + C
        Z1 = A * y_pred**2 + B * y_pred + C
        
        # Формування вектора Z для кожного параметра
        Z = np.zeros(p)
        for r in range(p):
            Z[r] = np.sum(Z1 * X_design[:, r])
        
        # Перевірка збіжності
        if np.linalg.norm(Z) < tol:
            converged = True
            if verbose:
                print(f"Збіжність досягнута на ітерації {iteration + 1}")
            break
        
        # Обчислення похідної JZ11 = 2*A*y_pred + B
        JZ11 = 2 * A * y_pred + B
        
        # Формування Якобіану
        Jacobian = np.zeros((p, p))
        for i in range(p):
            for j in range(p):
                Jacobian[i, j] = np.sum(JZ11 * X_design[:, i] * X_design[:, j])
        
        # Додавання регуляризації для числової стабільності
        if regularize:
            Jacobian += np.eye(p) * reg_lambda
        
        # Розв'язання системи Jacobian * delta = Z
        try:
            delta = solve(Jacobian, Z)
        except np.linalg.LinAlgError:
            if verbose:
                print("Warning: Не вдалося розв'язати систему. Використовую OLS оцінки.")
            return {
                'coefficients_ols': phi_ols,
                'coefficients_pmm2': phi_ols,
                'residuals_ols': residuals_ols,
                'residuals_pmm2': residuals_ols,
                'variance_ols': np.var(residuals_ols, ddof=p),
                'variance_pmm2': np.var(residuals_ols, ddof=p),
                'moments': moments,
                'variance_reduction': 0.0,
                'converged': False,
                'iterations': iteration + 1,
                'intercept': x_mean
            }
        
        # Оновлення параметрів
        phi_pmm2 = phi_pmm2 - delta
    
    if not converged and verbose:
        print(f"Warning: Не досягнуто збіжності за {max_iter} ітерацій")
    
    # Крок 7: Обчислення фінальних залишків і дисперсій
    residuals_pmm2 = y - X_design @ phi_pmm2
    
    var_ols = np.var(residuals_ols, ddof=p)
    var_pmm2 = np.var(residuals_pmm2, ddof=p)
    
    # Теоретичний коефіцієнт зменшення дисперсії
    # g = 1 - γ₃² / (2 + γ₄) для S=2
    g_theoretical = 1 - gamma3**2 / (2 + gamma4)
    
    # Емпіричне зменшення дисперсії
    variance_reduction = (1 - var_pmm2/var_ols) * 100 if var_ols > 0 else 0
    
    return {
        'coefficients_ols': phi_ols,
        'coefficients_pmm2': phi_pmm2,
        'residuals_ols': residuals_ols,
        'residuals_pmm2': residuals_pmm2,
        'variance_ols': var_ols,
        'variance_pmm2': var_pmm2,
        'moments': moments,
        'g_theoretical': g_theoretical,
        'variance_reduction': variance_reduction,
        'converged': converged,
        'iterations': iteration + 1 if converged else max_iter,
        'intercept': x_mean
    }


def monte_carlo_comparison(n_sims: int = 1000, n_obs: int = 200,
                           phi_true: float = 0.5,
                           error_dist: str = 'gamma',
                           verbose: bool = True) -> Dict:
    """
    Monte Carlo порівняння OLS vs PMM2 для AR(1) моделі.
    
    Parameters:
    -----------
    n_sims : int
        Кількість симуляцій
    n_obs : int
        Розмір вибірки
    phi_true : float
        Істинний параметр AR(1)
    error_dist : str
        Розподіл інновацій: 'gamma', 'lognormal', 'chisq', 'gaussian'
    verbose : bool
        Виводити прогрес
        
    Returns:
    --------
    results : dict
        Результати Monte Carlo симуляцій
    """
    phi_ols_estimates = []
    phi_pmm2_estimates = []
    var_reductions = []
    gamma3_values = []
    
    for sim in range(n_sims):
        if verbose and (sim + 1) % 100 == 0:
            print(f"Симуляція {sim + 1}/{n_sims}")
        
        # Генерація інновацій
        if error_dist == 'gamma':
            innovations = np.random.gamma(shape=2, scale=1, size=n_obs) - 2
        elif error_dist == 'lognormal':
            innovations = np.random.lognormal(mean=0, sigma=0.5, size=n_obs)
            innovations = innovations - np.mean(innovations)
        elif error_dist == 'chisq':
            innovations = np.random.chisquare(df=3, size=n_obs) - 3
        elif error_dist == 'gaussian':
            innovations = np.random.randn(n_obs)
        else:
            raise ValueError(f"Невідомий розподіл: {error_dist}")
        
        innovations = innovations - np.mean(innovations)
        
        # Генерація AR(1) ряду
        x = np.zeros(n_obs)
        x[0] = innovations[0] / np.sqrt(1 - phi_true**2)  # Стаціонарна ініціалізація
        for t in range(1, n_obs):
            x[t] = phi_true * x[t-1] + innovations[t]
        
        # Оцінювання
        try:
            results = fit_ar_pmm2_corrected(x, p=1, include_mean=True, verbose=False)
            
            phi_ols_estimates.append(results['coefficients_ols'][0])
            phi_pmm2_estimates.append(results['coefficients_pmm2'][0])
            var_reductions.append(results['variance_reduction'])
            gamma3_values.append(results['moments']['gamma3'])
            
        except Exception as e:
            if verbose:
                print(f"Помилка в симуляції {sim}: {e}")
            continue
    
    # Обчислення статистик
    phi_ols_arr = np.array(phi_ols_estimates)
    phi_pmm2_arr = np.array(phi_pmm2_estimates)
    
    results = {
        'n_successful': len(phi_ols_estimates),
        'phi_true': phi_true,
        
        # OLS статистики
        'ols_mean': np.mean(phi_ols_arr),
        'ols_std': np.std(phi_ols_arr),
        'ols_bias': np.mean(phi_ols_arr) - phi_true,
        'ols_mse': np.mean((phi_ols_arr - phi_true)**2),
        
        # PMM2 статистики
        'pmm2_mean': np.mean(phi_pmm2_arr),
        'pmm2_std': np.std(phi_pmm2_arr),
        'pmm2_bias': np.mean(phi_pmm2_arr) - phi_true,
        'pmm2_mse': np.mean((phi_pmm2_arr - phi_true)**2),
        
        # Відносна ефективність
        'relative_efficiency': np.var(phi_ols_arr) / np.var(phi_pmm2_arr),
        'mean_variance_reduction': np.mean(var_reductions),
        'median_variance_reduction': np.median(var_reductions),
        
        # Асиметрія
        'mean_gamma3': np.mean(gamma3_values),
        
        # Повні дані
        'phi_ols_estimates': phi_ols_arr,
        'phi_pmm2_estimates': phi_pmm2_arr,
        'variance_reductions': var_reductions,
        'gamma3_values': gamma3_values
    }
    
    return results


if __name__ == "__main__":
    print("=" * 70)
    print("PMM2 для AR(1) моделі - ВИПРАВЛЕНА ІМПЛЕМЕНТАЦІЯ")
    print("=" * 70)
    
    # Тест 1: Одна симуляція з детальним виводом
    print("\n=== ТЕСТ 1: Одна симуляція з Gamma інноваціями ===")
    np.random.seed(42)
    
    phi_true = 0.5
    n = 500
    innovations = np.random.gamma(2, 1, n) - 2
    innovations -= np.mean(innovations)
    
    x = np.zeros(n)
    x[0] = innovations[0] / np.sqrt(1 - phi_true**2)
    for t in range(1, n):
        x[t] = phi_true * x[t-1] + innovations[t]
    
    results = fit_ar_pmm2_corrected(x, p=1, include_mean=True, verbose=True)
    
    print(f"\nІстинний параметр: φ = {phi_true}")
    print(f"OLS оцінка:  φ̂ = {results['coefficients_ols'][0]:.4f}")
    print(f"PMM2 оцінка: φ̂ = {results['coefficients_pmm2'][0]:.4f}")
    print(f"Збіжність: {results['converged']} (ітерацій: {results['iterations']})")
    print(f"Зменшення дисперсії: {results['variance_reduction']:.2f}%")
    print(f"Теоретичний g: {results['g_theoretical']:.4f}")
    
    # Тест 2: Monte Carlo симуляції
    print("\n=== ТЕСТ 2: Monte Carlo симуляції (1000 повторень) ===")
    mc_results = monte_carlo_comparison(n_sims=1000, n_obs=200, 
                                        phi_true=0.5, error_dist='gamma',
                                        verbose=True)
    
    print(f"\n{'='*70}")
    print("РЕЗУЛЬТАТИ MONTE CARLO")
    print(f"{'='*70}")
    print(f"Успішних симуляцій: {mc_results['n_successful']}")
    print(f"Істинний параметр: φ = {mc_results['phi_true']}")
    print(f"Середня асиметрія: γ₃ = {mc_results['mean_gamma3']:.4f}")
    print()
    print("OLS:")
    print(f"  Середнє: {mc_results['ols_mean']:.4f}")
    print(f"  Стд.відх: {mc_results['ols_std']:.4f}")
    print(f"  Bias: {mc_results['ols_bias']:.4f}")
    print(f"  MSE: {mc_results['ols_mse']:.6f}")
    print()
    print("PMM2:")
    print(f"  Середнє: {mc_results['pmm2_mean']:.4f}")
    print(f"  Стд.відх: {mc_results['pmm2_std']:.4f}")
    print(f"  Bias: {mc_results['pmm2_bias']:.4f}")
    print(f"  MSE: {mc_results['pmm2_mse']:.6f}")
    print()
    print(f"Відносна ефективність: RE = {mc_results['relative_efficiency']:.4f}")
    print(f"Середнє зменшення дисперсії: {mc_results['mean_variance_reduction']:.2f}%")
    print(f"{'='*70}")
