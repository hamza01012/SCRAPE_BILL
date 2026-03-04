from bs4 import BeautifulSoup
import json

# file_name = "templates/mepcobill"

def scrape(text , app_no):
  try:

    soup = BeautifulSoup(text, "lxml") if text else None

    Top_Body = soup.find_all("div", class_="maincontent") if soup and soup.find_all("div", class_="maincontent") else None


    heading = Top_Body[0].find("div", class_="heading").find("h1") if Top_Body and Top_Body[0].find("div", class_="heading") else None

    # 1️⃣ Company name (remove span text)
    company_name = heading.find(string=True, recursive=False).strip() if heading else ""
    gst_block = heading.find("span").find(string=True, recursive=False).strip() if heading and heading.find("span") else ""
    gst_number = heading.find("span").find("br").next_sibling.strip() if heading and heading.find("span") and heading.find("span").find("br") else ""


    heading = Top_Body[0].find("div", class_="heading").find("div").find_all("b") if Top_Body and Top_Body[0].find("div", class_="heading") else None

    our_web_link = heading[1].text.strip() if len(heading) > 1 else ""

    First_table = soup.find("table",class_="maintable").find_all("tr")[1] if soup.find("table",class_="maintable") else None

    CONNECTION_DATE = First_table.find_all("td")[0].text.strip() if len(First_table.find_all("td")) > 0 else ""
    CONNECTED_LOAD_CURR_MDI = First_table.find_all("td")[1].text.strip() if len(First_table.find_all("td")) > 1 else ""
    ED = First_table.find_all("td")[2].text.strip() if len(First_table.find_all("td")) > 2 and len(First_table.find_all("td")[2].text.strip()) > 2 else ""
    BILL_MONTH = First_table.find_all("td")[3].text.strip() if len(First_table.find_all("td")) > 3 else ""
    READING_DATE = First_table.find_all("td")[4].text.strip() if len(First_table.find_all("td")) > 4 else ""
    ISSUE_DATE = First_table.find_all("td")[5].text.strip() if len(First_table.find_all("td")) > 5 else ""
    DUE_DATE = First_table.find_all("td")[6].text.strip() if len(First_table.find_all("td")) > 6 else ""



    table1 = soup.find("table",class_="nestable1").find_all("tr")[1] if soup.find("table",class_="nestable1") else None
    table2 = soup.find("table",class_="nestable1").find_all("tr")[3] if soup.find("table",class_="nestable1") else None

    CONSUMER_ID = table1.find_all("td")[0].text.strip() if table1 and len(table1.find_all("td")) > 0 else ""
    TARIFF = table1.find_all("td")[1].text.strip() if table1 and len(table1.find_all("td")) > 1 else ""
    LOAD = table1.find_all("td")[2].text.strip() if table1 and len(table1.find_all("td")) > 2 else ""
    OLD_A_C_NUMBER = table1.find_all("td")[3].text.strip() if table1 and len(table1.find_all("td")) > 3 else ""

    REFERENCE_NO = table2.find_all("td")[0].text.strip() if table2 and len(table2.find_all("td")) > 0 else ""
    LOCK_AGE = table2.find_all("td")[1].text.strip() if table2 and len(table2.find_all("td")) > 1 else ""
    NO_OF_ACS = table2.find_all("td")[2].text.strip() if table2 and len(table2.find_all("td")) > 2 else ""
    UN_BILL_AGE = table2.find_all("td")[3].text.strip() if table2 and len(table2.find_all("td")) > 3 else ""



    table = soup.find("h4", string="DIVISION").find_parent("table") if soup.find("h4", string="DIVISION") else None

    location_area = {}

    rows = table.find_all("tr") if table else []

    for row in rows:
        label = row.find("h4")
        value = row.find("td", class_="content")

        if label and value:
            key = label.get_text(strip=True)
            val = value.get_text(strip=True)
            location_area[key] = val


    maintable = soup.find_all("table",class_="maintable")[1] if len(soup.find_all("table",class_="maintable")) > 1 else None

    name_block = maintable.find("span", string="NAME & ADDRESS").find_parent("p") if maintable else None

    lines = [s.get_text(strip=True) for s in name_block.find_all("span")] if name_block else []

    # # remove first label line
    address_lines = [l for l in lines if l and l != "NAME & ADDRESS"]

    name = address_lines[0] if len(address_lines) > 0 else ""
    father = address_lines[1] if len(address_lines) > 1 else ""
    address1 = address_lines[2] if len(address_lines) > 2 else ""
    address2 = ", ".join(address_lines[3:]) if len(address_lines) > 3 else ""

    # URdu text is not being extracted properly, so we will keep it as is for now
    urdu_message = maintable.find("table", class_="nested4") if maintable.find("table", class_="nested4") else None
    urdu_message = urdu_message.find("strong").text.strip() if urdu_message and urdu_message.find("strong") else ""

    MCO_Date = maintable.find("h2", string="Say No To Corruption").find_parent("td").find("span").text.strip() if maintable and maintable.find("h2", string="Say No To Corruption") and maintable.find("h2", string="Say No To Corruption").find_parent("td") and maintable.find("h2", string="Say No To Corruption").find_parent("td").find("span") else ""

    meter_header = maintable.find("h4", string="METER NO").find_parent("tr") if maintable and maintable.find("h4", string="METER NO") else None
    meter_row = meter_header.find_next_sibling("tr") if meter_header else None

    cols = [c.get_text(strip=True) if c else "" for c in meter_row.find_all("td")] if meter_row else [""]*6 

    meter_data = {
        "meter_no": cols[0],
        "previous": cols[1],
        "present": cols[2],
        "mf": cols[3],
        "units": cols[4],
        "status": cols[5]
    }


    history_table = maintable.find("table", class_="nested6") if maintable else None

    rows = history_table.find_all("tr", class_="content") if history_table else []

    bill_month_history = []

    for r in rows:
        cols = [c.get_text(strip=True) if c else "" for c in r.find_all("td")]

        if len(cols) == 4:
            bill_month_history.append({
                "month": cols[0],
                "units": cols[1],
                "bill": cols[2],
                "payment": cols[3]
            })


    tables = soup.find_all("table", class_="nested7") if soup.find_all("table", class_="nested7") else []

    charges_table = tables[0]   # left table (charges breakdown)
    total_table   = tables[1]   # right table (bill totals)

    charges = {}

    rows = charges_table.find_all("tr") if charges_table else []

    for r in rows:
        cells = r.find_all("td")

        if len(cells) == 4:
            left_label  = cells[0].get_text(strip=True)
            left_value  = cells[1].get_text(strip=True)
            right_label = cells[2].get_text(strip=True)
            right_value = cells[3].get_text(strip=True)

            if left_label:
                charges[left_label] = left_value
            if right_label:
                charges[right_label] = right_value
        else:
            # Handle rows that don't have 4 cells (e.g., header rows)
            for i in range(0, len(cells)-1, 2):
                label = cells[i].get_text(strip=True)
                value = cells[i+1].get_text(strip=True)
                if label:
                    charges[label] = value

    totals = {}

    rows = total_table.find_all("tr") if total_table else []

    for r in rows:
        label = r.find("b")
        value = r.find("td", class_="content")

        if label and value:
            key = label.get_text(strip=True)
            val = value.get_text(strip=True)
            totals[key] = val

    td = total_table.find_all("td", class_="border-b nestedtd2width content")[-1].find("div").find_all("div") if total_table and total_table.find_all("td", class_="border-b nestedtd2width content") and total_table.find_all("td", class_="border-b nestedtd2width content")[-1].find("div") else []
    before_date = td[0].text.strip() if td else ""
    after_date = td[1].text.strip() if len(td) > 1 else ""


    totals["Payable just after Due Date"] = before_date
    totals["Payable after Due Date"] = after_date

    ALL_FOOTOR = soup.find("div", class_="headertable") if soup.find("div", class_="headertable") else None
    bill_number = ALL_FOOTOR.find("div").find("div").find("h4").text.replace("BILL NO :", "").strip() if ALL_FOOTOR and ALL_FOOTOR.find("div") and ALL_FOOTOR.find("div").find("div") and ALL_FOOTOR.find("div").find("div").find("h4") else ""

    content = ALL_FOOTOR.find_all("td") if ALL_FOOTOR else []

    CNIC = content[7] if len(content) > 7 else None


    file_name = "Bill_Scraperd/bill_data"

    with open(f"{file_name}.json", "r", encoding="utf-8") as f:
        existing_data = json.load(f)



    existing_data[CONSUMER_ID] = {
        "company_name": company_name,
        "gst_text": gst_block,
        "gst_number": gst_number,
        "our_web_link": our_web_link,
        "connection_date": CONNECTION_DATE,
        "connected_load_curr_mdi": CONNECTED_LOAD_CURR_MDI,
        "ed": ED,
        "bill_month": BILL_MONTH,
        "reading_date": READING_DATE,
        "issue_date": ISSUE_DATE,
        "due_date": DUE_DATE,
        "consumer_id": CONSUMER_ID,
        "tariff": TARIFF,
        "load": LOAD,
        "old_a_c_number": OLD_A_C_NUMBER,
        "reference_no": REFERENCE_NO,
        "lock_age": LOCK_AGE,
        "no_of_acs": NO_OF_ACS,
        "un_bill_age": UN_BILL_AGE,
        "location_area": location_area,
        "name": name,
        "father_name": father,
        "address1": address1,
        "address2": address2,
        "mco_date": MCO_Date,
        "meter_data": meter_data,
        "bill_month_history": bill_month_history,
        "charges": charges,
        "totals": totals,
        "cnic": CNIC.text.strip(),
        "bill_number": bill_number,
        "urdu_message": urdu_message
    }

    with open(f"{file_name}.json", "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)
    
    return {"success": True, "consumer_id": CONSUMER_ID,"reference_no": REFERENCE_NO, "bill_number": bill_number}

  except Exception as e:
      
      with open("Bill_Scraperd/scraper_errors.json", "r", encoding="utf-8") as f:
            existing_errors = json.load(f)

      existing_errors[app_no] = {"error": str(e)}

      with open("Bill_Scraperd/scraper_errors.json", "w", encoding="utf-8") as f:
            json.dump(existing_errors, f, indent=4, ensure_ascii=False)

      return {"error": "Failed to scrape bill data", "details": str(e)}    


