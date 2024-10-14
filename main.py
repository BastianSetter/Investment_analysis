from tester_utils import identifiy_variations, analyse_single_config, analyse_1D_variation, analyse_2D_variation

from example_blueprint import portfolio_blueprint_0d, portfolio_blueprint_1d



def main(portfolio_blueprint) -> None:
    base_portfolio, variations, counter = identifiy_variations(portfolio_blueprint)
    
    if counter == 0:
        analyse_single_config(base_portfolio)
    elif counter == 1:
        analyse_1D_variation(base_portfolio, variations[0])
    elif counter == 2:
        analyse_2D_variation(base_portfolio, variations)
    else:
        print('Too many variations.')



if __name__ == '__main__':
    main(portfolio_blueprint_0d)