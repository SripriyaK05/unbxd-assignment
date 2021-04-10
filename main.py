import requests
import json
import csv

url = "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?&q=*&rows=1&start=0"
res = requests.get(url)
# print(res.json())
# print(type(res.json()))
# print(res)
data = res.json()
number_of_products=data["response"]["numberOfProducts"]
rows= 500
# fdgfghjklm,cfhjbnm,fhgvjbn
# jgvjgvujgffjugtvffvf
print(number_of_products)
print("----------------")

def fetchColorPatch(x):
    a = x.split("::")
    return a[1]

def process_unbxd_products(products):
    for product in products:
        for key in product:
            # print(key)
            # print(product[key])
            if key == "unbxd_color_for_category":
                # for n in product["unbxd_color_for_category"]:
                #     a = "::".split(n)
                product["unbxd_color_for_category"] = list(map(fetchColorPatch, product["unbxd_color_for_category"]))

                # lambda x: "::".split(x)[1]
            if type(product[key]) is list:
                stringifiedLists = map(str, product[key])
                uniqueValues = dict.fromkeys(stringifiedLists)
                product[key] = ",".join(uniqueValues)

                # product[key] = ",".join(dict.fromkeys(map(str, product[key])))

            if type(product[key]) is bool:
                if product[key] is True:
                    product[key] = "YES"
                else:
                    product[key] = "NO"

            # print(product[key])
            # print("-------------")
    return products


def write_to_csv(final_products):
    with open('Sripriya-Unbxd-2021-Interns-Test.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(final_products[0].keys())
        for eachRow in final_products:
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


