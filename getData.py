#!/usr/bin/env python3
import gspread
import datetime
import sys
import textVariables
from oauth2client.service_account import ServiceAccountCredentials
from notifications import send_email_notification

# structs and global variables
emails = {
# email list of users to be notified
}

DATE_ROW = 2
USERS_COLUMN = 1
BALANCE_COLUMN = 2
BILL_AMOUNT = "$2.67"
DATE_FORMAT = "%d-%b-%Y"

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
		'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name\
			(textVariables.link_to_cred_json, scope)
my_spotify_spreadsheet = gspread.authorize(creds)

# get access to spotify sheet
spotify_sheet = my_spotify_spreadsheet.open("Spotify").sheet1

d = datetime.datetime.today()

def main () :
	# add_credit()
	# check if the new bill was made for the current month
	# new_bill_and_overdue_check(spotify_sheet)
	if len(sys.argv) > 1 :
		try :
			username = sys.argv[1]
			credit_amount = float(sys.argv[2])
			add_credit(username, credit_amount)
		except :
			print("Could not process your request for adding credit")
	else :
		if check_last_month_billed() != d.strftime("%b") :
			print("Charging new bill for ", d.strftime("%b"), " month")
			new_bill_and_overdue_check()
	return

def	add_credit(username, credit_amount) :
	cell = spotify_sheet.find(username)
	cell_row = int(cell.row)
	cell_col = int(cell.col)
	add_credit_to_col = cell_col + 1
	add_credit_to_row = cell_row
	change_message_on_col = cell_col
	change_message_on_row = cell_row + 1

	# print("Adding ", "$"+str(credit_amount), " to ", username)
	print("Adding ${credit} to {name}".format(credit = credit_amount, name = username))

	# change message
	message = "Added ${credit} on {day}".format(credit = credit_amount, day = d.strftime(DATE_FORMAT))
	spotify_sheet.update_cell(change_message_on_row, change_message_on_col, message)

	# add credit value
	current_credit = float(spotify_sheet.cell(add_credit_to_row, \
						add_credit_to_col).value[1:]) + credit_amount
	spotify_sheet.update_cell(add_credit_to_row, add_credit_to_col, current_credit)

	send_email_notification(username, emails[username], credit_amount)
	return

def check_last_month_billed() :
	last_mont_billed_column_index = int(next_available_column()) - 1
	date = spotify_sheet.cell(DATE_ROW, last_mont_billed_column_index).value
	return date.split('-')[1]


def new_bill_and_overdue_check() :
	# make a new bill for todays date
	next_column = next_available_column()
	spotify_sheet.update_cell(DATE_ROW, next_column, d.strftime(DATE_FORMAT))
	for bill_index in range(3,12) :
		if bill_index % 2 :
			spotify_sheet.update_cell(bill_index, next_column, BILL_AMOUNT)

	# Extract indecies with negative values
	users_with_negative_balance = {}
	list_of_balance = spotify_sheet.col_values(BALANCE_COLUMN)
	list_of_users = spotify_sheet.col_values(USERS_COLUMN)

	# assign dictionary key : value pairs for users with overdue balance
	for balance_index in range(2, len(list_of_balance)) :
		if balance_index % 2 :
			if list_of_balance[balance_index][0] == '-' :
				users_with_negative_balance[list_of_users[balance_index-1]] = \
				list_of_balance[balance_index]

	if len(users_with_negative_balance) != 0 :
		print("there are users with balance overdue")

	# send emails to users with uverdue balance
	for user in users_with_negative_balance :
		try :
			send_email_notification(user, emails[user], -1 * float(users_with_negative_balance[user][2:]))
		except :
			print("Could not send the notification email")
	return

def next_available_column() :
	str_list = [i for i in spotify_sheet.row_values(DATE_ROW)]
	return str(len(str_list) + 1)

if __name__ == '__main__' :
	main()
