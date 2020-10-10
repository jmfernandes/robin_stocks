"""Contains functions for getting all the information tied to a user account."""
import robin_stocks.helper as helper
import robin_stocks.urls as urls


@helper.login_required
def load_account_profile(info=None):
    """Gets the information associated with the accounts profile,including day
    trading information and cash being held by Robinhood.

    :param info: The name of the key whose value is to be returned from the function.
    :type info: Optional[str]
    :returns: The function returns a dictionary of key/value pairs. \
    If a string is passed in to the info parameter, then the function will return \
    a string corresponding to the value of the key whose name matches the info parameter.
    :Dictionary Keys: * url
                      * portfolio_cash
                      * can_downgrade_to_cash
                      * user
                      * account_number
                      * type
                      * created_at
                      * updated_at
                      * deactivated
                      * deposit_halted
                      * only_position_closing_trades
                      * buying_power
                      * cash_available_for_withdrawal
                      * cash
                      * cash_held_for_orders
                      * uncleared_deposits
                      * sma
                      * sma_held_for_orders
                      * unsettled_funds
                      * unsettled_debit
                      * crypto_buying_power
                      * max_ach_early_access_amount
                      * cash_balances
                      * margin_balances
                      * sweep_enabled
                      * instant_eligibility
                      * option_level
                      * is_pinnacle_account
                      * rhs_account_number
                      * state
                      * active_subscription_id
                      * locked
                      * permanently_deactivated
                      * received_ach_debit_locked
                      * drip_enabled
                      * eligible_for_fractionals
                      * eligible_for_drip
                      * eligible_for_cash_management
                      * cash_management_enabled
                      * option_trading_on_expiration_enabled
                      * cash_held_for_options_collateral
                      * fractional_position_closing_only
                      * user_id
                      * rhs_stock_loan_consent_status

    """
    url = urls.account_profile()
    data = helper.request_get(url, 'indexzero')
    return(helper.filter(data, info))


@helper.login_required
def load_basic_profile(info=None):
    """Gets the information associated with the personal profile,
    such as phone number, city, marital status, and date of birth.

    :param info: The name of the key whose value is to be returned from the function.
    :type info: Optional[str]
    :returns: The function returns a dictionary of key/value pairs. If a string \
    is passed in to the info parameter, then the function will return a string \
    corresponding to the value of the key whose name matches the info parameter.
    :Dictionary Keys: * user
                      * address
                      * city
                      * state
                      * zipcode
                      * phone_number
                      * marital_status
                      * date_of_birth
                      * citizenship
                      * country_of_residence
                      * number_dependents
                      * signup_as_rhs
                      * tax_id_ssn
                      * updated_at

    """
    url = urls.basic_profile()
    data = helper.request_get(url)
    return(helper.filter(data, info))


@helper.login_required
def load_investment_profile(info=None):
    """Gets the information associated with the investment profile.
    These are the answers to the questionaire you filled out when you made your profile.

    :param info: The name of the key whose value is to be returned from the function.
    :type info: Optional[str]
    :returns: The function returns a dictionary of key/value pairs. \
    If a string is passed in to the info parameter, then the function will return \
    a string corresponding to the value of the key whose name matches the info parameter.
    :Dictionary Keys: * user
                      * total_net_worth
                      * annual_income
                      * source_of_funds
                      * investment_objective
                      * investment_experience
                      * liquid_net_worth
                      * risk_tolerance
                      * tax_bracket
                      * time_horizon
                      * liquidity_needs
                      * investment_experience_collected
                      * suitability_verified
                      * option_trading_experience
                      * professional_trader
                      * understand_option_spreads
                      * interested_in_options
                      * updated_at

    """
    url = urls.investment_profile()
    data = helper.request_get(url)
    return(helper.filter(data, info))


@helper.login_required
def load_portfolio_profile(info=None):
    """Gets the information associated with the portfolios profile,
    such as withdrawable amount, market value of account, and excess margin.

    :param info: The name of the key whose value is to be returned from the function.
    :type info: Optional[str]
    :returns: The function returns a dictionary of key/value pairs. \
    If a string is passed in to the info parameter, then the function will return \
    a string corresponding to the value of the key whose name matches the info parameter.
    :Dictionary Keys: * url
                      * account
                      * start_date
                      * market_value
                      * equity
                      * extended_hours_market_value
                      * extended_hours_equity
                      * extended_hours_portfolio_equity
                      * last_core_market_value
                      * last_core_equity
                      * last_core_portfolio_equity
                      * excess_margin
                      * excess_maintenance
                      * excess_margin_with_uncleared_deposits
                      * excess_maintenance_with_uncleared_deposits
                      * equity_previous_close
                      * portfolio_equity_previous_close
                      * adjusted_equity_previous_close
                      * adjusted_portfolio_equity_previous_close
                      * withdrawable_amount
                      * unwithdrawable_deposits
                      * unwithdrawable_grants

    """
    url = urls.portfolio_profile()
    data = helper.request_get(url, 'indexzero')
    return(helper.filter(data, info))


@helper.login_required
def load_security_profile(info=None):
    """Gets the information associated with the security profile.

    :param info: The name of the key whose value is to be returned from the function.
    :type info: Optional[str]
    :returns: The function returns a dictionary of key/value pairs. \
    If a string is passed in to the info parameter, then the function will return \
    a string corresponding to the value of the key whose name matches the info parameter.
    :Dictionary Keys: * user
                      * object_to_disclosure
                      * sweep_consent
                      * control_person
                      * control_person_security_symbol
                      * security_affiliated_employee
                      * security_affiliated_firm_relationship
                      * security_affiliated_firm_name
                      * security_affiliated_person_name
                      * security_affiliated_address
                      * security_affiliated_address_subject
                      * security_affiliated_requires_duplicates
                      * stock_loan_consent_status
                      * agreed_to_rhs
                      * agreed_to_rhs_margin
                      * rhs_stock_loan_consent_status
                      * updated_at

    """
    url = urls.security_profile()
    data = helper.request_get(url)
    return(helper.filter(data, info))


@helper.login_required
def load_user_profile(info=None):
    """Gets the information associated with the user profile,
    such as username, email, and links to the urls for other profiles.

    :param info: The name of the key whose value is to be returned from the function.
    :type info: Optional[str]
    :returns: The function returns a dictionary of key/value pairs. \
    If a string is passed in to the info parameter, then the function will return \
    a string corresponding to the value of the key whose name matches the info parameter.
    :Dictionary Keys: * url
                      * id
                      * id_info
                      * username
                      * email
                      * email_verified
                      * first_name
                      * last_name
                      * origin
                      * profile_name
                      * created_at

    """
    url = urls.user_profile()
    data = helper.request_get(url)
    return(helper.filter(data, info))
