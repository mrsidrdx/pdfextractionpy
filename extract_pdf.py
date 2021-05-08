import pdfplumber
import sys
from pprint import pprint
import json

# python extract_pdf.py test.pdf test.json

def index_in_list(a_list, index):
    return index < len(a_list)

with pdfplumber.open('input_files/' + sys.argv[1]) as pdf:

    extracted_data_json = {}

    page_count = 0
    page_table_no = 0

    page = pdf.pages[page_count]
    first_text = page.extract_text(x_tolerance=3, y_tolerance=3).split('\n')
    extracted_data_json["UIN"] = first_text[4].split(': ')[1]
    tables = page.extract_tables()

    # Transaction Details

    transaction_details_table = tables[page_table_no]
    extracted_data_json['Transaction Details'] = []
    for i in range(2, len(transaction_details_table)):
        temp_dict = {
            "TransactionNo": transaction_details_table[i][1],
            "TransactionDate ": transaction_details_table[i][2],
            "Parent UIN": transaction_details_table[i][2]
        }
        extracted_data_json['Transaction Details'].append(temp_dict)

    while(True):
        if not index_in_list(tables, page_table_no + 1):
            page_table_no = 0
            page_count += 1
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            if tables[page_table_no][0][0] == 'Party Details':
                break
            transaction_details_table = tables[page_table_no]
            for i in range(0, len(transaction_details_table)):
                temp_dict = {
                    "TransactionNo": transaction_details_table[i][1],
                    "TransactionDate ": transaction_details_table[i][2],
                    "Parent UIN": transaction_details_table[i][2]
                }
                extracted_data_json['Transaction Details'].append(temp_dict)
        else:
            page_table_no += 1
            break
        

    # Party Details

    party_details_table = tables[page_table_no]
    extracted_data_json['PartyDetails'] = {
        'IndianParties' : [],
        'ForeignParties' : [],
        'DetailsofOtherIndianParties' : []
    }
    row_no = 3
    while(True):
        if not index_in_list(party_details_table, row_no):
            page_table_no = 0
            page_count += 1
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            row_no = 0
            party_details_table = tables[page_table_no]
            if party_details_table[row_no][1] == None:
                row_no += 1
        elif party_details_table[row_no][1] == None:
            row_no += 1
            break
        else:
            temp_dict = {
                "NameoftheParty": party_details_table[row_no][1].replace('\n', ''),
                "AddressoftheParty": party_details_table[row_no][2].replace('\n', ''),
                "NetWorth": party_details_table[row_no][3].replace('\n', ''),
                "StakeofJVorWOS": party_details_table[row_no][4].replace('\n', '')
            }
            extracted_data_json['PartyDetails']['IndianParties'].append(temp_dict)
            row_no += 1

    while(True):
        if not index_in_list(party_details_table, row_no):
            page_table_no = 0
            page_count += 1
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            row_no = 0
            party_details_table = tables[page_table_no]
            if party_details_table[row_no][1] == None:
                row_no += 1
        elif party_details_table[row_no][1] == None:
            row_no += 1
            break
        else:
            temp_dict = {
                "NameoftheParty": party_details_table[row_no][1].replace('\n', ''),
                "AddressoftheParty": party_details_table[row_no][2].replace('\n', ''),
                "NetWorth": party_details_table[row_no][3].replace('\n', ''),
                "StakeofJVorWOS": party_details_table[row_no][4].replace('\n', '')
            }
            extracted_data_json['PartyDetails']['ForeignParties'].append(temp_dict)
            row_no += 1

    while(True):
        if not index_in_list(party_details_table, row_no):
            if index_in_list(tables, page_table_no + 1):
                page_table_no += 1
                break
            page_table_no = 0
            page_count += 1
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            row_no = 0
            party_details_table = tables[page_table_no]
            if party_details_table[row_no][1] == None:
                row_no += 1
        elif party_details_table[row_no][1] == None:
            row_no += 1
            break
        else:
            temp_dict = {
                "NameoftheParty": party_details_table[row_no][1].replace('\n', ''),
                "AddressoftheParty": party_details_table[row_no][2].replace('\n', ''),
                "NetWorth": party_details_table[row_no][3].replace('\n', ''),
                "StakeofJVorWOS": party_details_table[row_no][4].replace('\n', '')
            }
            extracted_data_json['PartyDetails']['DetailsofOtherIndianParties'].append(temp_dict)
            row_no += 1

    # Details of Overseas Concern

    overseas_concern_table = tables[page_table_no]
    overseas_concern_list = [
        "Name",
        "Address",
        "Category",
        "Country",
        "Activity",
        "SubActivity",
        "NatureofInvestment",
        "Accounting Year",
        "AuthorizedDealer",
        "StatusoftheUIN"
    ]
    extracted_data_json['DetailsofOverseasConcern'] = {
        "Name": "",
        "Address": "",
        "Category": "",
        "Country": "",
        "Activity": "",
        "SubActivity": "",
        "NatureofInvestment": "",
        "Accounting Year": "",
        "AuthorizedDealer": "",
        "StatusoftheUIN": ""
    }

    row_no, count = 1, 0
    while(True):
        if not index_in_list(overseas_concern_table, row_no):
            if index_in_list(tables, page_table_no + 1):
                page_table_no += 1
                break
            page_table_no = 0
            page_count += 1
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            row_no = 0
            overseas_concern_table = tables[page_table_no]
            if overseas_concern_table[row_no][0] == 'INDIAN PARTIES UNDER INVESTIGATION':
                break
        else:
            if count == 10:
                if not index_in_list(tables, page_table_no + 1):
                    page_table_no = 0
                    page_count += 1
                    page = pdf.pages[page_count]
                    tables = page.extract_tables()
                else:
                    page_table_no += 1
                break
            else:
                extracted_data_json['DetailsofOverseasConcern'][overseas_concern_list[count]] = overseas_concern_table[row_no][2].replace('\n', '')
                row_no += 1
                count += 1


    # INDIAN PARTIES UNDER INVESTIGATION

    indian_parties_under_investigation_table = tables[page_table_no]
    extracted_data_json["IndianPartiesUnderInvestigation"] = {
        "IndianParty": []
    }
    row_no = 2
    temp_dict = {}
    while(True):
        if not index_in_list(indian_parties_under_investigation_table, row_no):
            if index_in_list(tables, page_table_no + 1):
                page_table_no += 1
                break
            page_table_no = 0
            page_count += 1
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            row_no = 0
            indian_parties_under_investigation_table = tables[page_table_no]
            if indian_parties_under_investigation_table[row_no][0] == 'Change in name of the Indian party':
                break
        else:
            while(True):
                if not index_in_list(indian_parties_under_investigation_table, row_no):
                    if len(temp_dict) > 0:
                        extracted_data_json["IndianPartiesUnderInvestigation"]["IndianParty"].append(temp_dict)
                    break
                elif indian_parties_under_investigation_table[row_no][1] == None:
                    if len(temp_dict) > 0:
                        extracted_data_json["IndianPartiesUnderInvestigation"]["IndianParty"].append(temp_dict)
                    temp_dict = {
                        "IndianPartyName" : indian_parties_under_investigation_table[row_no][0].split(':')[1].strip(),
                        "InvestigationData" : []
                    }
                    row_no += 1
                else:
                    period_data = indian_parties_under_investigation_table[row_no][2].split(':')
                    to_date = period_data[-1].strip()
                    from_date = period_data[1].split('To')[0].strip()
                    temp_data = {
                        "NameoftheInvestigationAgency": indian_parties_under_investigation_table[row_no][1],
                        "PeriodUnderInvestigation": {
                            "From": from_date,
                            "To": to_date
                        }
                    }
                    row_no += 1
                    temp_dict["InvestigationData"].append(temp_data)

    # Change in name of the Indian party

    change_indian_party_table = tables[page_table_no]
    extracted_data_json["ChangeInNameOfTheIndianParty"] = []
    row_no = 2
    while True:
        if not index_in_list(change_indian_party_table, row_no):
            if index_in_list(tables, page_table_no + 1):
                page_table_no += 1
                break
            page_table_no = 0
            page_count += 1
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            row_no = 0
            change_indian_party_table = tables[page_table_no]
            if change_indian_party_table[row_no][0] == 'Change in name of JV / WOS':
                break
        else:
            temp_dict = {
                "OldName": change_indian_party_table[row_no][1].replace('\n', ''),
                "NewName": change_indian_party_table[row_no][2].replace('\n', ''),
                "ModifiedDate": change_indian_party_table[row_no][3].replace('\n', ''),
                "wef": change_indian_party_table[row_no][4].replace('\n', ''),
                "UserType": change_indian_party_table[row_no][5].replace('\n', '')
            }
            extracted_data_json["ChangeInNameOfTheIndianParty"].append(temp_dict)
            row_no += 1

    # Change in name of JV / WOS

    change_jv_wos_table = tables[page_table_no]
    extracted_data_json["ChangeInNameOfJVorWOS"] = []
    row_no = 2
    while True:
        if not index_in_list(change_jv_wos_table, row_no):
            if index_in_list(tables, page_table_no + 1):
                page_table_no += 1
                break
            page_table_no = 0
            page_count += 1
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            row_no = 0
            change_jv_wos_table = tables[page_table_no]
            if change_jv_wos_table[row_no][0] == 'Approved Investments':
                break
        else:
            temp_dict = {
                "OldName": change_jv_wos_table[row_no][1].replace('\n', ''),
                "NewName": change_jv_wos_table[row_no][2].replace('\n', ''),
                "ModifiedDate": change_jv_wos_table[row_no][3].replace('\n', ''),
                "wef": change_jv_wos_table[row_no][4].replace('\n', ''),
                "UserType": change_jv_wos_table[row_no][5].replace('\n', '')
            }
            extracted_data_json["ChangeInNameOfJVorWOS"].append(temp_dict)
            row_no += 1

    # Approved Investments

    approved_investments_table = tables[page_table_no]
    approved_investments_list = [
        "Equity",
        "Loan",
        "GuaranteeIssued",
        "GuaranteeInvoked"
    ]
    extracted_data_json["ApprovedInvestments"] = {
        "Equity": '',
        "Loan": '',
        "GuaranteeIssued": '',
        "GuaranteeInvoked": ''
    }
    row_no, count = 1, 0
    while True:
        if not index_in_list(approved_investments_table, row_no):
            if index_in_list(tables, page_table_no + 1):
                page_table_no += 1
                break
            page_table_no = 0
            page_count += 1
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            row_no = 0
            approved_investments_table = tables[page_table_no]
            if approved_investments_table[row_no][0] == 'Financial Commitment':
                break
        else:
            extracted_data_json["ApprovedInvestments"][approved_investments_list[count]] = approved_investments_table[row_no][2]
            row_no += 1
            count += 1

    # Financial Commitment
    
    financial_commitment_table = tables[page_table_no]
    extracted_data_json['FinancialCommitment'] = []
    row_no = 3
    while True:
        if not index_in_list(financial_commitment_table, row_no):
            if index_in_list(tables, page_table_no + 1):
                page_table_no += 1
                break
            page_table_no = 0
            page_count += 1
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            row_no = 0
            financial_commitment_table = tables[page_table_no]
            if financial_commitment_table[row_no][0] == 'Part II Transactions (Outflow) "Pending for RBI Ratification/Approval"':
                break
        else:
            if financial_commitment_table[row_no][0] == 'Total':
                if not index_in_list(financial_commitment_table, row_no+1):
                    row_no += 1
                else:
                    page_table_no += 1
                    break
            else:
                temp_dict = {
                    "IPName": financial_commitment_table[row_no][1].replace('\n', ''),
                    "TranNo": financial_commitment_table[row_no][2].replace('\n', ''),
                    "DateofFinancialCommitment": financial_commitment_table[row_no][3].replace('\n', ''),
                    "DateofReporting": financial_commitment_table[row_no][4].replace('\n', ''),
                    "Source": financial_commitment_table[row_no][5].replace('\n', ''),
                    "CUR": financial_commitment_table[row_no][6].replace('\n', ''),
                    "FinancialCommitmentInActual": {
                        "Equity": financial_commitment_table[row_no][7].replace('\n', ''),
                        "Loan": financial_commitment_table[row_no][8].replace('\n', ''),
                        "GuaranteeInvoked": financial_commitment_table[row_no][9].replace('\n', ''),
                        "GuaranteeIssued": financial_commitment_table[row_no][10].replace('\n', ''),
                        "GuaranteeStatuses": financial_commitment_table[row_no][11].replace('\n', '')
                    }
                }
                extracted_data_json["FinancialCommitment"].append(temp_dict)
                row_no += 1

    # Part II Transactions (Outflow) "Pending for RBI Ratification/Approval"

    rbi_ratification_table = tables[page_table_no]
    extracted_data_json['PendingforRBIRatificationApproval'] = []
    row_no = 3
    while True:
        if not index_in_list(rbi_ratification_table, row_no):
            if index_in_list(tables, page_table_no + 1):
                page_table_no += 1
                break
            page_table_no = 0
            page_count += 1
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            row_no = 0
            rbi_ratification_table = tables[page_table_no]
            if rbi_ratification_table[row_no][0] == 'Inflow Details':
                break
        else:
            if rbi_ratification_table[row_no][0] == 'Total':
                if not index_in_list(rbi_ratification_table, row_no+1):
                    row_no += 1
                else:
                    page_table_no += 1
                    break
            else:
                temp_dict = {
                    "IPName": rbi_ratification_table[row_no][1].replace('\n', ''),
                    "TranNo": rbi_ratification_table[row_no][2].replace('\n', ''),
                    "DateofFinancialCommitment": rbi_ratification_table[row_no][3].replace('\n', ''),
                    "DateofReporting": rbi_ratification_table[row_no][4].replace('\n', ''),
                    "Source": rbi_ratification_table[row_no][5].replace('\n', ''),
                    "CUR": rbi_ratification_table[row_no][6].replace('\n', ''),
                    "FinancialCommitmentInActual": {
                        "Equity": rbi_ratification_table[row_no][7].replace('\n', ''),
                        "Loan": rbi_ratification_table[row_no][8].replace('\n', ''),
                        "GuaranteeInvoked": rbi_ratification_table[row_no][9].replace('\n', ''),
                        "GuaranteeIssued": rbi_ratification_table[row_no][10].replace('\n', ''),
                        "GuaranteeStatuses": rbi_ratification_table[row_no][11].replace('\n', '')
                    }
                }
                extracted_data_json["PendingforRBIRatificationApproval"].append(temp_dict)
                row_no += 1

    # Inflow Details

    inflow_details_table = tables[page_table_no]
    extracted_data_json['Inflow Details'] = []
    row_no = 2
    while True:
        if not index_in_list(inflow_details_table, row_no):
            if index_in_list(tables, page_table_no + 1):
                page_table_no += 1
                break
            page_table_no = 0
            page_count += 1
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            row_no = 0
            inflow_details_table = tables[page_table_no]
            if inflow_details_table[row_no][0] == 'Submission of APR':
                break
        else:
            if inflow_details_table[row_no][0] == 'Total':
                if not index_in_list(inflow_details_table, row_no+1):
                    row_no += 1
                else:
                    page_table_no += 1
                    break
            else:
                temp_dict = {
                    "Date": inflow_details_table[row_no][1].replace('\n', ''),
                    "Component": inflow_details_table[row_no][2].replace('\n', ''),
                    "Amount": inflow_details_table[row_no][3].replace('\n', '')
                }
                extracted_data_json["Inflow Details"].append(temp_dict)
                row_no += 1

    # Submission of APR

    apr_submission_table = tables[page_table_no]
    extracted_data_json['SubmissionofAPR'] = []
    row_no = 2
    while True:
        if not index_in_list(apr_submission_table, row_no):
            if index_in_list(tables, page_table_no + 1):
                page_table_no += 1
                break
            page_table_no = 0
            page_count += 1
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            row_no = 0
            apr_submission_table = tables[page_table_no]
            if apr_submission_table[row_no][0] == 'Change in A/cing year of the overseas subsidiary. Last five changes':
                break
        else:
            temp_dict = {
                "Transaction No": apr_submission_table[row_no][1].replace('\n', ''),
                "StartDatOfAccountingPeriod ": apr_submission_table[row_no][2].replace('\n', ''),
                "EndDatOfAccountingPeriod ": apr_submission_table[row_no][3].replace('\n', ''),
                "AccountingYear": apr_submission_table[row_no][4].replace('\n', ''),
                "Status": apr_submission_table[row_no][5].replace('\n', ''),
                "SubmittedOrRatification Date": apr_submission_table[row_no][6].replace('\n', '')
            }
            extracted_data_json["SubmissionofAPR"].append(temp_dict)
            row_no += 1

    # Change in A/cing year of the overseas subsidiary. Last five changes

    overseas_subsidiary_table = tables[page_table_no]
    extracted_data_json['ChangeInOverseasSubsidary'] = []
    row_no = 2
    while True:
        if not index_in_list(overseas_subsidiary_table, row_no):
            if index_in_list(tables, page_table_no + 1):
                page_table_no += 1
                break
            page_table_no = 0
            page_count += 1
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            row_no = 0
            overseas_subsidiary_table = tables[page_table_no]
            if overseas_subsidiary_table[row_no][0] == 'Disinvestment details':
                break
        else:
            temp_dict = {
                "OldAccountingYear": overseas_subsidiary_table[row_no][1].replace('\n', ''),
                "NewAccountingYear": overseas_subsidiary_table[row_no][2].replace('\n', ''),
                "ModificationDate": overseas_subsidiary_table[row_no][3].replace('\n', ''),
                "EffectiveDate": overseas_subsidiary_table[row_no][4].replace('\n', ''),
                "UserType": overseas_subsidiary_table[row_no][5].replace('\n', '')
            }
            extracted_data_json["ChangeInOverseasSubsidary"].append(temp_dict)
            row_no += 1

    # Disinvestment details

    disinvestment_details_table = tables[page_table_no]
    extracted_data_json['DisinvestmentDetails'] = []
    row_no = 2
    while True:
        if not index_in_list(disinvestment_details_table, row_no):
            if index_in_list(tables, page_table_no + 1):
                page_table_no += 1
                break
            page_table_no = 0
            page_count += 1
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            row_no = 0
            disinvestment_details_table = tables[page_table_no]
            if disinvestment_details_table[row_no][0] == 'Details of conversion of loan into Equity and equity into loan':
                break
        else:
            amount_repatriated = disinvestment_details_table[row_no][5].replace('\n', '').split('-')[-1].strip().split(' ')
            amount = amount_repatriated[1]
            currency = amount_repatriated[0]
            temp_dict = {
                "UINNumber": disinvestment_details_table[row_no][1].replace('\n', ''),
                "TransactionNumber ": disinvestment_details_table[row_no][2].replace('\n', ''),
                "DateOfDisinvestment": disinvestment_details_table[row_no][3].replace('\n', ''),
                "DateOfRepatriated": disinvestment_details_table[row_no][4].replace('\n', ''),
                "AmountRepatriated": {
                    "Equity": {
                        "Amount": amount,
                        "CUR": currency
                    }
                }
            }
            extracted_data_json["DisinvestmentDetails"].append(temp_dict)
            row_no += 1

    # Details of conversion of loan into Equity and equity into loan

    loan_equity_conversion_table = tables[page_table_no]
    extracted_data_json['ConversionOfLoanToEquityAndEquityToLoan'] = []
    row_no = 2
    while True:
        if not index_in_list(loan_equity_conversion_table, row_no):
            if index_in_list(tables, page_table_no + 1):
                page_table_no += 1
                break
            page_table_no = 0
            page_count += 1
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            row_no = 0
            loan_equity_conversion_table = tables[page_table_no]
            if loan_equity_conversion_table[row_no][0] == 'Guarantee Details':
                break
        else:
            temp_dict = {
                "TransactionNo ": loan_equity_conversion_table[row_no][1].replace('\n', ''),
                "OriginalRemittanceDate": loan_equity_conversion_table[row_no][2].replace('\n', ''),
                "OriginalAmount": loan_equity_conversion_table[row_no][3].replace('\n', ''),
                "DateOfConversion": loan_equity_conversion_table[row_no][4].replace('\n', ''),
                "ModifiedAmount": loan_equity_conversion_table[row_no][5].replace('\n', ''),
                "Remarks": loan_equity_conversion_table[row_no][6].replace('\n', ''),
                "UserType": loan_equity_conversion_table[row_no][7].replace('\n', '')
            }
            extracted_data_json["ConversionOfLoanToEquityAndEquityToLoan"].append(temp_dict)
            row_no += 1

    # Guarantee Details

    guarantee_details_table = tables[page_table_no]
    extracted_data_json['GuaranteeDetails'] = []
    row_no = 2
    while True:
        if not index_in_list(guarantee_details_table, row_no):
            if index_in_list(tables, page_table_no + 1):
                page_table_no += 1
                break
            page_table_no = 0
            page_count += 1
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            row_no = 0
            guarantee_details_table = tables[page_table_no]
            if guarantee_details_table[row_no][0] == 'Step down subsidiary details':
                break
        else:
            temp_dict = {
                "TransactionNo ": guarantee_details_table[row_no][1].replace('\n', ''),
                "MethodOfInvestment ": guarantee_details_table[row_no][2].replace('\n', ''),
                "CategoryOfInvestment ": guarantee_details_table[row_no][3].replace('\n', ''),
                "ForeignCurrencyCode ": guarantee_details_table[row_no][4].replace('\n', ''),
                "GuaranteeAmount ": guarantee_details_table[row_no][5].replace('\n', ''),
                "GuaranteeIssueDate": guarantee_details_table[row_no][6].replace('\n', ''),
                "GuaranteeValidityDate ": guarantee_details_table[row_no][7].replace('\n', ''),
                "GuaranteeIssuesInFavour": guarantee_details_table[row_no][8].replace('\n', ''),
                "GuaranteeIssueRoute": guarantee_details_table[row_no][9].replace('\n', '')
            }
            extracted_data_json["GuaranteeDetails"].append(temp_dict)
            row_no += 1

    # Step down subsidiary details

    stepdown_details_table = tables[page_table_no]
    extracted_data_json['StepDownDetails'] = []
    row_no = 2
    while True:
        if not index_in_list(stepdown_details_table, row_no):
            if index_in_list(tables, page_table_no + 1):
                page_table_no += 1
                break
            page_table_no = 0
            page_count += 1
            if page_count >= len(pdf.pages):
                break
            page = pdf.pages[page_count]
            tables = page.extract_tables()
            row_no = 0
            stepdown_details_table = tables[page_table_no]
        else:
            if stepdown_details_table[row_no][0] == 'No':
                row_no += 1
            else:
                temp_dict = {
                    "LevelOfStepDownSubsidiary": stepdown_details_table[row_no][1].replace('\n', ''),
                    "SDSName ": stepdown_details_table[row_no][2].replace('\n', ''),
                    "Country ": stepdown_details_table[row_no][3].replace('\n', ''),
                    "Stake ": stepdown_details_table[row_no][4].replace('\n', ''),
                    "OperatingOrSPV ": stepdown_details_table[row_no][5].replace('\n', ''),
                    "ParentCompanyName ": stepdown_details_table[row_no][6].replace('\n', '')
                }
                extracted_data_json["StepDownDetails"].append(temp_dict)
                row_no += 1

    # print(extracted_data_json)

    # Serializing json 
    json_object = json.dumps(extracted_data_json, indent = 4)
    
    # Writing to sample.json
    with open('output_json/' + sys.argv[2], "w") as outfile:
        outfile.write(json_object)

    # pprint(tables)


