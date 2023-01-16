# Apostilles using signed, encrypted QR codes

## Introduction

*What are apostilles?* The _Apostille_ convention of 5 October 1961 ("Abolishing the Requirement of Legalisation for Foreign Public Documents") is an international treaty intended to simplify the procedure through which a document issued in one of the contracting states can be certified for legal purposes in all the other contracting states. An apostilled document simply contains a stamp that confirms the validity of the information and should be accepted internationally.

*The problem:* However, in many countries, the process of receiving and apostille is complicated, costly and slow, and the transfer of information is often difficult because documents are not standardised, machine-readable, nor is the stamp verifiable easily (e.g., digitally signed). Furthermore, entering the information on an apostilled document into a different state's information system is often prone to errors (a secretary has to type it by hand), and as the fields are not standardised, can lead to significant questions on how to deal with the information.

*Aims:* The following document is aimed at describing an upgrade to the current apostille stamp system. In its most simplified form, documents and their fields will be standardised, include internationalised scrips, be machine-readable and be digitally signed (using QR codes).

## Principles

Document fields should be saved in JSON, with standardised fields for each document type. UTF-8 is used for internationalised character encoding.

The JSON string is then converted to a Base64 string, signed by the issued, encrypted and compressed. Then, a QR code is generated. The public key is available openly.

In the receiving office/country, the QR code can be read, with the document contents verified using the signature. Then, the fields are transferred to the receiving country's computer system automatically (thanks to the standardisation) and a new document in that country's format can be issued on the spot.

In order for the documents to be easily transferrable, the name fields will contain both a simple ASCII (latin alphabet, English) version as is common in passports and identification documents (in the machine-readable strip), and in any set of additional languages for special symbols or scripts. Language-specific fields are specified using the ISO 639-3 three-letter language codes.

As the document QR codes can be readily decrypted and read, it is the responsibility of the document owner who they provide the documents to.

## Examples of common documents

Note that all the name fields can have internationalised versions for special characters/alphabets, as mentioned above

### Birth certificate

When a child is born, the issuing authority (hospital, population office, judge or similar) scans the machine-readable strips of identity documents (ID or passport) of both parents.

The following fields are automatically added based on this information:
1. *Citizenship(s):* A child usually carries the citizenships of both parents, and in some cases that of the place of birth. Note that some countries add the citizenship of a place or province of origin in a secondary field
2. *Surname and surname format:* Multiple options are available here, but this is typically determined automatically based on the citizenship. In the case of multiple citizenships, the one of the options is chosen out of all the allowable ones from the countries of citizenship. Options are the following:
   1. Surname of the father (e.g., common in Germany)
   2. Surname of the mother (e.g., accepted alternative to (1) in Switzerland)
   3. Given name of the father (e.g., common in India, Ethiopia)
   4. Given name of the mother
   5. Combined surname of father, then mother (e.g., common in Spain). Note here that in the case where the parents have a combined surname, one part of it has to be chosen to pass on to the child. For example, the first surname of a combined surname in Spain is the father's and is typically passed to a child. These surnames are typically separated by a space.
   6. Combined surname of mother, then father
   7. Other (e.g., clan name): Entered manually
3. Issuing authority:
   1. Name of issuing authority
   2. City/place, province
   3. Country
   
The following fields are entered manually by the issuing authority:
1. First name, provided by the parents
2. Date of birth
3. Gender

Example birth certificate:
```
{
  "firstName": "Juerg",
  "firstName-deu": "Jürg"
  "lastName": "Mustermann",
  "dateOfBirth": "1970-01-01",
  "surnameType": "surnameOfFather",
  "gender": "M",
  "parents": [
    {
      "firstName": "Hans",
      "lastName": "Mustermann",
      "dateOfBirth": "1945-01-01",
    },
    {
      "firstName": "Anna",
      "lastName": "Example",
      "dateOfBirth": "1950-01-01",
    }
  ],
  "issueDate": "2022-07-01",
  "issuingAuthority": "Population Registry",
  "issuingAuthority-deu": "Einwohnerkontrolle",
  "issuingPlace": "Zuerich",
  "issuingPlace-deu": "Zürich",
  "issuingCountry": "CHE",
  "documentType": "birthCertificate"
}
```

### Marriage certificate

The marriage officer scans the machine-readable strips of identity documents (ID or passport) of both spouses (and his own, should this be the first officiated marriage).

The following fields are then provided automatically:
1. For both spouses:
   1. First (given) name
   2. Surname before marriage (maiden name)
   3. Date of birth
   4. Number of identity document and issuing country
   5. Citizenship
2. For the marriage officer:
   1. First (given) name
   2. Surname
3. About the marriage:
   1. Date
   2. City/place, province
   3. Country
   4. Name of issuing authority (e.g., religious authority, population registration center, judge)
   5. Date of issue of the document

The field for the surname after marriage may need to be updated manually. Some countries offer options to chose from, while others do not. The following options are accepted and are either selected automatically based on the law of the country of marriage or of citizenship(s), or are chosen if multiple options are available in those countries:
1. Maiden surname kept
2. Surname of other spouses
3. First name of other spouse
4. Combined name, enter combination character (e.g. space, dash)

### Certificate of civil status / singleness

This document is sometimes also called a *letter of non-impediment*, and confirms that a person is either married or single (or divorced). It is typically issued by the country/countries of citizenship. The following fields are available:

1. Information about the person:
   1. First (given) name
   2. Surname
   3. Maiden name (empty if not applicable)
   4. Date of birth
   5. Gender
   6. Citizenship (including that of a place/province, if required)
2. Civil status. The following are accepted:
   1. Single
   2. Married
   3. Divorced
   4. Widowed
   5. Date of last change of status required. Birth date if single
3. Details on the spouse, if applicable:
   1. Given name(s)
   2. Surname
   3. Maiden name
   4. Birth date
   5. Gender
   6. Citizenship
4. Details on the parents:
   1. Given name(s)
   2. Surnames
   3. Birth dates
5. Issuing authority:
   1. Name of issuing authority
   2. Issuing country
   3. Date of issue of the document
   
```
{
  "firstName": "Jonathan",
  "firstName-heb": "יונתן"
  "lastName": "Cohen",
  "lastName-heb": "כהן",
  "maidenName": null,
  "dateOfBirth": "1990-02-03",
  "gender": "M",
  "citizenship": "ISR",
  "civilStatus": "married"
  "civilStatusChange": "2015-03-01"
  "spouse": {
     "firstName": "Anne",
     "firstName-heb": "חנה"
     "lastName": "Cohen",
     "lastName-heb": "כהן",
     "maidenName": Martin,
     "dateOfBirth": "1992-03-04",
     "gender": "F",
     "citizenship": "FRE"
  },
  "parents": [
    {
      "firstName": "Daniel",
	  "firstName-heb": "דניאל"
      "lastName": "Cohen",
      "lastName-heb": "כהן",
      "dateOfBirth": "1945-01-01",
    },
    {
      "firstName": "Abigail",
	  "firstName-heb": "אביגיל‎"
      "lastName": "Cohen",
      "lastName-heb": "כהן",
      "dateOfBirth": "1950-01-01",
    }
  ],
  "issueDate": "2022-07-01",
  "issuingAuthority": "Ministry of Interior",
  "issuingAuthority-heb": "משרד הפנים",
  "issuingPlace": "Tel Aviv",
  "issuingCountry": "ISR",
  "documentType": "certificateCivilStatus"
}
```

Corresponding Base64:
```
ewogICJmaXJzdE5hbWUiOiAiSm9uYXRoYW4iLAogICJmaXJzdE5hbWUtaGViIjogIteZ15XXoNeq158iCiAgImxhc3ROYW1lIjogIkNvaGVuIiwKICAibGFzdE5hbWUtaGViIjogIteb15TXnyIsCiAgIm1haWRlbk5hbWUiOiBudWxsLAogICJkYXRlT2ZCaXJ0aCI6ICIxOTkwLTAyLTAzIiwKICAiZ2VuZGVyIjogIk0iLAogICJjaXRpemVuc2hpcCI6ICJJU1IiLAogICJjaXZpbFN0YXR1cyI6ICJtYXJyaWVkIgogICJjaXZpbFN0YXR1c0NoYW5nZSI6ICIyMDE1LTAzLTAxIgogICJzcG91c2UiOiB7CiAgICAgImZpcnN0TmFtZSI6ICJBbm5lIiwKICAgICAiZmlyc3ROYW1lLWhlYiI6ICLXl9eg15QiCiAgICAgImxhc3ROYW1lIjogIkNvaGVuIiwKICAgICAibGFzdE5hbWUtaGViIjogIteb15TXnyIsCiAgICAgIm1haWRlbk5hbWUiOiBNYXJ0aW4sCiAgICAgImRhdGVPZkJpcnRoIjogIjE5OTItMDMtMDQiLAogICAgICJnZW5kZXIiOiAiRiIsCiAgICAgImNpdGl6ZW5zaGlwIjogIkZSRSIKICB9LAogICJwYXJlbnRzIjogWwogICAgewogICAgICAiZmlyc3ROYW1lIjogIkRhbmllbCIsCgkgICJmaXJzdE5hbWUtaGViIjogIteT16DXmdeQ15wiCiAgICAgICJsYXN0TmFtZSI6ICJDb2hlbiIsCiAgICAgICJsYXN0TmFtZS1oZWIiOiAi15vXlNefIiwKICAgICAgImRhdGVPZkJpcnRoIjogIjE5NDUtMDEtMDEiLAogICAgfSwKICAgIHsKICAgICAgImZpcnN0TmFtZSI6ICJBYmlnYWlsIiwKCSAgImZpcnN0TmFtZS1oZWIiOiAi15DXkdeZ15LXmdec4oCOIgogICAgICAibGFzdE5hbWUiOiAiQ29oZW4iLAogICAgICAibGFzdE5hbWUtaGViIjogIteb15TXnyIsCiAgICAgICJkYXRlT2ZCaXJ0aCI6ICIxOTUwLTAxLTAxIiwKICAgIH0KICBdLAogICJpc3N1ZURhdGUiOiAiMjAyMi0wNy0wMSIsCiAgImlzc3VpbmdBdXRob3JpdHkiOiAiTWluaXN0cnkgb2YgSW50ZXJpb3IiLAogICJpc3N1aW5nQXV0aG9yaXR5LWhlYiI6ICLXntep16jXkyDXlNek16DXmdedIiwKICAiaXNzdWluZ1BsYWNlIjogIlRlbCBBdml2IiwKICAiaXNzdWluZ0NvdW50cnkiOiAiSVNSIiwKICAiZG9jdW1lbnRUeXBlIjogImNlcnRpZmljYXRlQ2l2aWxTdGF0dXMiCn0=
```

### Criminal record

The following fields are available:
1. First (given) name
2. Surname
3. Date of birth
4. Citizenship
5. Criminal record empty (yes/no). If it is not empty, refer to printed fields on the document
6. Date of issue
7. Name of issuing authority
8. Issuing country

Example criminal record with international names:
```
{
  "firstName": "Juerg",
  "firstName-deu": "Jürg"
  "lastName": "Mustermann",
  "dateOfBirth": "1970-01-01",
  "citizenship": "CHE",
  "criminalRecord": False,
  "issueDate": "2023-01-01",
  "issuingAuthority": "Department of Justice",
  "issuingAuthority-deu": "Bundesamt für Justiz",
  "issuingPlace": "Bern",
  "issuingCountry": "CHE",
  "documentType": "excerptCriminalRecord"
}
```

### Driving license

The following fields are available:

1. Information about the person:
   1. First (given) name
   2. Surname
   3. Date of birth
   4. Citizenship (including of place/province, if required)
2. Information about the license:
   1. Date of issue of the license
   2. Date of expiry of the license
   3. Issuing authority
   4. Issuing country
3. Categories:
   1. Categories A to E are accepted, according to the 1968 International Convention relative to Motor Traffic
   2. Date of issue, for each category
   3. Date of expiry, for each category
4. Code for additional restrictions (e.g., requiring glasses)

### Certificate of current/completed studies

1. Information about the person:
   1. First (given) name
   2. Surname
   3. Date of birth
   4. Citizenship (including that of a place/province, if required)
   5. Identity document or passport number
2. Details on studies:
   1. Type of degree (e.g. High School, professional license, BSc, MSc, PhD, Postdoc)
   2. Title of degree
   3. Starting date
   4. End date (empty if currently studying for this degree)
   5. Faculty
   6. Department
   7. Advisor (e.g. required for PhD, Postdoc)
3. Details on issuing educational institution:
   1. Name of School/University
   2. Place/City, Province
   3. Country
   4. Date of issue


## License

This software and documents are distributed under the Creative Commons Zero v1.0 Universal, i.e. the document and code can be freely distributed, used and modified without any copyright restrictions (see license file).

