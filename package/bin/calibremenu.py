#Author:	Shaz
#Purpose:	Creates a command line menu to add, remove or search for books in a Calibre Library using
#			the Calibre content server daemon. Means you don't need access to GUI and
#			can manage a Calibre library via SSH on a Raspberry Pi.
#Date: 		07/05/2015
#Version:	1.0.0

import os, subprocess, shutil

#store the temp folder which has the book(s) to add and the path to the calibre library
#raspberry pi paths
path_to_books = "/home/pi/books-to-add/" #Amend this path to where the book you want to add is found
path_to_library = "/mnt/calibre-library" #amend this path to the location of your calibre library

#--------CLASSES--------
	
class calibreBooks(object):
	
	#Check if a string is numeric (used by the removeBook function)
	def isnumeric(self, ids_response):
		try:
			float(ids_response)
			return True
		except ValueError:
			return False
			
	#FUNCTION TO ADD BOOKS TO CALIBRE
	def addBooks(self):
		print "Are you sure you want to add book(s) to Calibre? Y/n \n"
		response = raw_input("> ")

		if response == "y":
			print "Adding...\n"
			subprocess.check_output(["calibredb", "add", "-r", path_to_books, "--with-library", path_to_library])
			print "Done...\n"
			
			#prompt to empty the directory which has the book file
			prompt_to_empty_folder = calibreBooks() #create an instance of calibreBooks class
			prompt_to_empty_folder.deleteBookFromFolder() #from class instance get the function deleteBookFromFolder with arg self

		elif response == "n":
			return calibreMenu()
	
		else:
			addBooks()
	
	#FUNCTION TO DELETE CONTENTS OF path_to_books FOLDER (used by addBooks function)
	def deleteBookFromFolder(self):	
		print "Empty directory %s? Y/n" % path_to_books
		empty_folder = raw_input("> ")
		if empty_folder == "y":
			for file_object in os.listdir(path_to_books):
				file_object_path = os.path.join(path_to_books, file_object)
				if os.path.isfile(file_object_path):
					os.unlink(file_object_path)
				else:
					shutil.rmtree(file_object_path)
			print "Done...\n"
	
		elif empty_folder == "n":
			return calibreMenu()
	
		else:
			deleteBookFromFolder()
	
	#FUNCTION TO DELETE BOOKS		
	def removeBook(self):
		print "Enter IDS of the book to delete."
		ids_response = raw_input("> ")
		
		#check if the input is numeric	
		check_integer = calibreBooks()		
		if check_integer.isnumeric(ids_response):
			print "Removing...\n"
			subprocess.check_output(["calibredb", "remove", ids_response, "--with-library", path_to_library])
			print "Done...\n"
		
		#if not numeric then prompt to search
		else:
			print "Invalid IDS number.\n Search for book by keyword instead to obtain IDS?\n y to proceed\n n to go back to removing\n q to go back to Calibre Menu\n"
			keyword_response = raw_input("> ")
			if keyword_response == "y":
				search_by_keyword = calibreBooks() #create an instance of class calibreBooks by assigning to variable search_by_keyword
				search_by_keyword.keywordSearch(ids_response)
				
				return_to_removing_book = calibreBooks()
				return_to_removing_book.removeBook()
				
			elif keyword_response == "n":
				#global return_to_removing_book 
				return_to_removing_book = calibreBooks()
				return_to_removing_book.removeBook()
				
			elif keyword_response == "q":
				go_back = calibreMenu()
				return go_back
			
	#FUNCTIONS TO SEARCH BY KEYWORD, TITLE AND AUTHOR
	def keywordSearch(self, keyword_response):
		print "Searching...\n"
		keyword_result = subprocess.check_output(["calibredb", "list", "--search", '"%s"' % (keyword_response), "--with-library", path_to_library])
		print keyword_result
	
	def titleSearch(self, titleSearch_response):
		print "Searching...\n"
		titleSearch_result = subprocess.check_output(["calibredb", "list", "--search", 'title:"%s"' % (titleSearch_response), "--with-library", path_to_library])
		print titleSearch_result

	def authorSearch(self, authorSearch_response):
		print "Searching...\n"
		authorSearch_result = subprocess.check_output(["calibredb", "list", "--search", 'author:"%s"' % (authorSearch_response), "--with-library", path_to_library])
		print authorSearch_result

#---------FUNCTIONS--------

#FUNCTION FOR MAIN CALIBRE MENU
def calibreMenu():
	print "---------------------------"
	print "  CalibreDB Menu"
	print "---------------------------"
	print "1. Add Book(s)"
	print "2. Remove book"
	print "3. Search library"
	print "4. Exit\n"
	
	response = raw_input("> ")
	
	if response == "1":
		add_book = calibreBooks()
		add_book.addBooks()
		calibreMenu()
	
	elif response == "2":
		remove_book = calibreBooks()
		remove_book.removeBook()
		calibreMenu()
	
	elif response == "3":
		calibreSearch()
	
	elif response == "4":
		exit()

	else:
		calibreMenu()

#FUNCTION FOR SEARCH MENU	
def calibreSearch():
	print "---------------------------"
	print "  CalibreDB Search"
	print "---------------------------"
	print "1. Search by keyword"
	print "2. Search by title"
	print "3. Search by author"
	print "4. Return to Main Menu\n"
		
	search_by = raw_input("> ")
	if search_by == "1":
		print "Enter keyword to search?"
		keyword_response = raw_input("> ")
		search = calibreBooks()
		search.keywordSearch(keyword_response)
		print "Done..."
		calibreSearch()
			
			
	elif search_by == "2":
		print "Enter title to search?"
		titleSearch_response = raw_input("> ")
		search = calibreBooks()
		search.titleSearch(titleSearch_response)
		print "Done..."
		calibreSearch()
			
	elif search_by == "3":
		print "Enter author to search?"
		authorSearch_response = raw_input("> ")
		search = calibreBooks()
		search.authorSearch(authorSearch_response)
		print "Done..."
		calibreSearch()

	elif search_by == "4":
		calibreMenu()

#--------MAIN----------

#Begin with the main CalibreDB Menu
calibreMenu()