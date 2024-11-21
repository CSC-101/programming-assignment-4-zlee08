import sys

import build_data

import hw3

import os

def print_data(list):
    for x in list:
        print(x.county, x.state)
        print("{:>20} {} {}".format("", "Population: ",x.population.get("2014 Population")))
        print("{:>20} {}".format("", "Age"))
        print("{:>30} {} {}".format("", "<5:",x.age.get("Percent 65 and Older")))
        print("{:>30} {} {}".format("", "<18:",x.age.get("Percent Under 18 Years")))
        print("{:>30} {} {}".format("", ">65:",x.age.get("Percent Under 5 Years")))
        print("{:>20} {}".format("", "Education"))
        print("{:>30} {} {}".format("", ">= High School:",x.education.get("High School or Higher")))
        print("{:>30} {} {}".format("", ">= Bachelor:",x.education.get("Bachelor's Degree or Higher")))
        print("{:>20} {}".format("", "Ethnicity Percentages"))
        print("{:>30} {} {}{}".format("", "American Indian and Alaska Native Alone:",x.ethnicities.get("American Indian and Alaska Native Alone"),"%"))
        print("{:>30} {} {}{}".format("", "Asian Alone:",x.ethnicities.get("Asian Alone"),"%"))
        print("{:>30} {} {}{}".format("", "Black Alone:",x.ethnicities.get("Black Alone"),"%"))
        print("{:>30} {} {}{}".format("", "Hispanic or Latino:",x.ethnicities.get("Hispanic or Latino"),"%"))
        print("{:>30} {} {}{}".format("", "Native Hawaiian and Other Pacific Islander Alone:",x.ethnicities.get("Native Hawaiian and Other Pacific Islander Alone"),"%"))
        print("{:>30} {} {}{}".format("", "Two or More Races:",x.ethnicities.get("Two or More Races"),"%"))
        print("{:>30} {} {}{}".format("", "White Alone:",x.ethnicities.get("White Alone"),"%"))
        print("{:>30} {} {}{}".format("", "White Alone, not Hispanic or Latino:",x.ethnicities.get("White Alone, not Hispanic or Latino"),"%"))
        print("{:>20} {}".format("", "Income"))
        print("{:>30} {} {}".format("", "Per Capita:",x.income.get("Per Capita Income")))
        print("{:>30} {} {}".format("", "Below Poverty Level:",x.income.get("Persons Below Poverty Level")))
        print("{:>30} {} {}".format("", "Median Household:",x.income.get("Median Household Income")))


def field_decoder (list,field,percent):
    field = field.replace("\n","")
    items = field.split(".")
    group = items[0]
    data = items[1]
    if group == "Education":
        if percent:
            results = hw3.percent_by_education(list,data)
        else:
            results = hw3.population_by_education(list,data)
    if group == "Ethnicities":
        if percent:
            results = hw3.percent_by_ethnicity(list,data)
        else:
            results = hw3.population_by_ethnicity(list,data)
    if group == "Income":
        if percent:
            results = hw3.percent_below_poverty_level(list)
        else:
            results = hw3.population_below_poverty_level(list)
    return results

def field_filter (list,field,percent,criteria):
    field = field.replace("\n","")
    items = field.split(".")
    group = items[0]
    data = items[1]
    results = []
    if group == "Education":
       if criteria == "gt":
          results = [x for x in list if x.education.get(data) > percent]
       else:
          results = [x for x in list if x.education.get(data) < percent]
    if group == "Ethnicities":
      if criteria == "gt":
          results = [x for x in list if x.ethnicities.get(data) > percent]
      else:
          results = [x for x in list if x.ethnicities.get(data) < percent]
    if group == "Income":
      if criteria == "gt":
          results = [x for x in list if x.income.get(data) > percent]
      else:
          results = [x for x in list if x.income.get(data) < percent]
    return results

def process_file(filename):
    full_data= build_data.get_data()
    print(str(len(full_data)) + " records loaded")
    with open(filename, 'r') as f:
        var = []
        for line in f:
            line = line.replace("\n","")
            sl = line.split(":")
            if sl[0] == "display":
                print_data(full_data)
            if sl[0] == "population-total":
                pop = hw3.population_total(full_data)
                print("2014 population: " + str(pop))
            if sl[0] == "filter-state":
                state = sl[1]
                full_data = hw3.filter_by_state(full_data,state)
                print("Filter: " + state + " == " + sl[1] + " (" + str(len(full_data)) + " entries)")
            if sl[0] == "population":
                field = sl[1]
                results = field_decoder(full_data,field,0)
                print("2014 " +  field + " population: " + str(results))
            if sl[0] == "percent":
                field = sl[1]
                results = field_decoder(full_data,field,1)
                print("2014 " +  field + " percentage: " + str(results))
            if sl[0] == "filter-gt":
                field = sl[1]
                num = float(sl[2])
                full_data = field_filter(full_data,field,num,"gt")
                print("Filter " + sl[1] + " gt " + str(num) + " (" + str(len(full_data)) + " entries)")
            if sl[0] == "filter-lt":
                field = sl[1]
                num = float(sl[2])
                full_data = field_filter(full_data,field,num,"lt")
                print("Filter " + sl[1] + " lt " + str(num) + " (" + str(len(full_data)) + " entries)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
     print("Please type an operation file as an argument.")
     sys.exit(1)
    else:
     if os.path.exists(sys.argv[1]):
          process_file(sys.argv[1])
     else:
          print("The file does not exist or cannot be opened.")
          sys.exit(1)