# import the installed requests  library
import requests
import json
# The csv library provides functionality to both read from and write to CSV files
import csv

# To make a ‘GET’ request, we’ll use the requests.get() function, which requires one argument — the URL we want to make the request to.
url = "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?&q=*&rows=1&start=0"
res = requests.get(url)
# The documentation tells us that the API response we’ll get is in JSON format.
data = res.json()
# here it fetches the number of products from response and it is stored in number_of_products variable
number_of_products=data["response"]["numberOfProducts"]
rows= 500
print("the total number of products found is : ",number_of_products)
print("----------------")

# here we have created a function named fetchcolorpath and it split fucntion is used to split array and a[1] index value is printed
def fetchColorPatch(x):
    a = x.split("::")
    return a[1]

def process_unbxd_products(products):
    # Extract the `products` object from `response` object in the response
    # A for loop is used for iterate over a object products
    for product in products:
        # A for loop is used for iterate over a each product key and value
        for key in product:
            # For `unbxd_color_for_category` key, before merging them into string if its an array, split the value by `::` and add only the color value into the final string

            if key == "unbxd_color_for_category":
                # in if condition the key value is checked wheather it is equal to unbxd_color_for_category,if the condition is true then it maped by passing function fetchcolorpatch and product[key]
                # The map() function executes a specified function for each item in an iterable.
                # list is used to list the array values
                product["unbxd_color_for_category"] = list(map(fetchColorPatch, product["unbxd_color_for_category"]))
                # Convert all array type data structures to string separated by `,`.If same value already present in the array, then ignore them from final string
                # here we are checking wheater the product[key] is list


            if type(product[key]) is list:
                #  map converts the array to string and its stored in a variable stringifiedLists
                stringifiedLists = map(str, product[key])
                # and here dict.formkeys is used that removes the duplicate values from  stringifiedlists because dict do not allow duplicate values.
                uniqueValues = dict.fromkeys(stringifiedLists)
                # join fucntion is used seperate string by ','
                product[key] = ",".join(uniqueValues)


            # If the value of a property is boolean like `true` or `false`, then convert such values to `YES` & `NO`.
            # here first we are checking wheater the product[key] contains boolean values

            if type(product[key]) is bool:
                # if the product[key]  is boolean it returns true and checka next if loop
                # in next loop if product[key]=True then it prints product[key]=Yes
                if product[key] is True:
                    product[key] = "YES"
                # in else condition the product[key] will be equal to False and it changes to NO
                else:
                    product[key] = "NO"
    return products


#write_to_csv function is created its called in function after all the operations performed to convert to csv file
def write_to_csv(final_products):
    # The CSV file is opened as a text file with Python’s built-in open() function, which returns a file object. This is then passed in writing mode
    with open('Sripriya-Unbxd-2021-Interns-Test.csv', 'w') as csv_file:
        # The csv.writer() function returns a writer object that converts the user's data into a delimited string.
        csv_writer = csv.writer(csv_file, delimiter=',')
        # list is passed to the writer.writerows() method to write the content of the list to the CSV file here it returns the key
        csv_writer.writerow(final_products[0].keys())
        # for loop is used  to iterate through each products
        for eachRow in final_products:
            # the writer.writerows() method to write the content of the list to the CSV file here it returns the values
            csv_writer.writerow(eachRow.values())
        csv_file.close()


def main():
    final_products=list()
    for start in range(0,number_of_products,rows):
        print("Fetching Data from " + str(start+1) + " to " + str(start+rows))
        url = "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?&q=*&rows="+ str(rows) +"&start="+ str(start)
        res = requests.get(url)
        data = res.json()
        products = data["response"]["products"]

        response = process_unbxd_products(products)
        final_products.extend(response)
    write_to_csv(final_products)
    print(final_products)


main()


