# Apostilles using signed, encrypted QR codes

## Introduction

*What are apostilles?* The _Apostille_ convention of 5 October 1961 ("Abolishing the Requirement of Legalisation for Foreign Public Documents") is an international treaty intended to simplify the procedure through which a document issued in one of the contracting states can be certified for legal purposes in all the other contracting states. An apostilled document simply contains a stamp that confirms the validity of the information and should be accepted internationally.

*The problem:* However, in many countries, the process of receiving and apostille is complicated, costly and slow, and the transfer of information is often difficult because documents are not standardised, machine-readable, nor is the stamp verifiable easily (e.g., digitally signed). Furthermore, entering the information on an apostilled document into a different state's information system is often prone to errors (a secretary has to type it by hand), and as the fields are not standardised, can lead to significant questions on how to deal with the information.

*Aims:* The following document is aimed at describing an upgrade to the current apostille stamp system. In its most simplified form, documents and their fields will be standardised, include internationalised scrips, be machine-readable and be digitally signed (using QR codes).

## Principles

Document fields should be saved in JSON, with standardised fields for each document type. UTF-8 is used for internationalised character encoding.

The JSON string is then converted to a Base64 string, signed by the issued and encrypted. The public key is available openly. 

In the receiving office/country, the QR code can be read, with the document contents verified using the signature. Then, the fields are transferred to the receiving country's computer system automatically (thanks to the standardisation) and a new document in that country's format can be issued on the spot.

In order for the documents to be easily transferrable, the name fields will contain both a simple ASCII (latin alphabet, English) version as is common in passports and identification documents (in the machine-readable strip), and in any set of additional languages for special symbols or scripts. Language-specific fields are specified using the ISO 639-3 three-letter language codes.

## Examples

### Birth certificate

When a child is born, the issuing authority (hospital, population office, judge or similar) scans the machine-readable strips of identity documents (ID or passport) of both parents. The following fields are automatically added based on this information:
1. Citizenship(s): A child usually carries the citizenships of both parents, and in some cases that of the place of birth
2. Surname:

The only fields that are entered are the date of birth, location, name of the issuing authority and issuing country.

Surname and citizenship is automatically assessed using the parents' documents.

### Marriage certificate

### Criminal record

### Driving license


## License

This software and documents are distributed under the Creative Commons Zero v1.0 Universal, i.e. the document and code can be freely distributed, used and modified without any copyright restrictions (see license file).

