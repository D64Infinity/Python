package main

import (
	"fmt"
	"log"
	"net/http"
	"strings"
	"time"

	"github.com/PuerkitoBio/goquery"
	"github.com/xuri/excelize/v2"
)

func main() {
	input := "Links.xlsx"
	output := "result.xlsx"

	in, err := excelize.OpenFile(input)
	if err != nil {
		log.Fatal(err)
	}

	sheetName := in.GetSheetName(0)
	rows, err := in.GetRows(sheetName)
	if err != nil {
		log.Fatal(err)
	}

	out := excelize.NewFile()
	sheet := out.GetSheetName(0)

	out.SetSheetRow(sheet, "A1", &[]string{
		"Ссылка", "Название", "IMO", "MMSI", "Тип",
	})

	rowIndex := 2

	for i := 1; i < len(rows); i++ {
		if len(rows[i]) == 0 {
			continue
		}

		link := strings.TrimSpace(rows[i][0])
		if link == "" {
			continue
		}

		fmt.Println("Checking:", link)

		resp, err := http.Get(link)
		if err != nil {
			continue
		}

		doc, err := goquery.NewDocumentFromReader(resp.Body)
		resp.Body.Close()
		if err != nil {
			continue
		}

		vesselTotalsText := strings.TrimSpace(doc.Find(".pagination-totals").Text()) //block with info about amount of found vessels
		if vesselTotalsText != "" && !strings.HasPrefix(vesselTotalsText, "1 ") {
			continue
		}

		var vesselLinks []string
		doc.Find("a").Each(func(_ int, s *goquery.Selection) { //counting hrefs with "/vessels/" substring
			href, ok := s.Attr("href")
			if ok && strings.Contains(href, "/vessels/") {
				vesselLinks = append(vesselLinks, href)
			}
		})

		if len(vesselLinks) != 1 {
			continue
		}

		detailURL := "https://www.vesselfinder.com" + vesselLinks[0]
		time.Sleep(500 * time.Millisecond)

		resp, err = http.Get(detailURL)
		if err != nil {
			continue
		}

		doc, err = goquery.NewDocumentFromReader(resp.Body)
		resp.Body.Close()
		if err != nil {
			continue
		}

		title := strings.TrimSpace(doc.Find("title").Text())

		keyPart := strings.Split(title, " - ")[0]
		nt := strings.SplitN(keyPart, ",", 2) //nt stands for "name type"

		name := strings.TrimSpace(nt[0])
		vtype := strings.TrimSpace(nt[1]) //vtype stands for "vessel type"
		imo := findValue(doc, "IMO")
		mmsi := findValue(doc, "MMSI")

		out.SetSheetRow(sheet, fmt.Sprintf("A%d", rowIndex),
			&[]string{link, name, imo, mmsi, vtype})
		rowIndex++
	}

	out.SaveAs(output)
	fmt.Println("Результат записан в файл:", output)
}

func findValue(doc *goquery.Document, label string) string {
	var value string
	doc.Find("td").Each(func(_ int, s *goquery.Selection) {
		if strings.Contains(s.Text(), label) {
			value = strings.TrimSpace(s.Next().Text())
		}
	})
	return value
}
