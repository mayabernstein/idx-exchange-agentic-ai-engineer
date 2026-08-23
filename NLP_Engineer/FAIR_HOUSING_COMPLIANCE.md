# Fair Housing Compliance Guidelines

## 1. Purpose

The Fair Housing Compliance Checker is designed to identify potentially discriminatory or exclusionary language in real-estate listing descriptions before publication.

The checker is a screening tool that helps to identify language that may require revision or human review, but it does not make a legal determination that a listing violates the Fair Housing Act.

## 2. Fair Housing Requirements

The Fair Housing Act prohibits discrimination in housing based on protected characteristics, including:

* Race
* Color
* National origin
* Religion
* Sex
* Familial status
* Disability

Listing descriptions should describe the property, its features, location, and amenities rather than expressing preferences for or against particular groups of people.

## 3. Examples of Potentially Prohibited Language

Examples of language that should be removed or investigated include:

### Familial Status

Potentially prohibited examples:

* "No children"
* "Adults only"
* "Children not allowed"
* "No kids"

These statements can indicate that families with children are being excluded.

### Disability

Potentially prohibited examples:

* "No wheelchairs"
* "Must be able-bodied"
* "Wheelchairs not allowed"

Property descriptions should instead describe objective accessibility characteristics of the property.

### Race or Color

Potentially prohibited examples:

* "White neighborhood"
* "White community"
* "Whites only"

Listing descriptions should not indicate a preference for or exclusion of people based on race or color.

### Religion

Potentially prohibited examples:

* "Christian community"
* "Jewish neighborhood"
* "Muslim community"

Religious characteristics of a neighborhood should not be used to indicate who would be preferred as a resident.

### Sex or Gender

Potentially prohibited examples:

* "Men only"
* "Women only"
* "Females only"

Such language can indicate an exclusion based on sex or gender and should be reviewed.

### National Origin

Potentially prohibited examples:

* "Native-born only"
* "Americans only"

Listing descriptions should not express preferences based on national origin.

## 4. Compliance Checker Severity Levels

The ComplianceChecker uses three severity levels.

### Error

An `error` indicates clear potentially prohibited or exclusionary language.

In this case, the listing should not be published until the language has been removed or appropriately revised within the listing description.

Example:

> "Adults only community."

Result:

```text
severity: error
can_publish: false
```

### Warning

A `warning` indicates language that may be problematic depending on its context.

In this case, a human reviewer should examine the listing before publication.

Example:

> "Perfect for singles."

Result:

```text
severity: warning
can_publish: true
```

The listing can be held for review rather than automatically treated as a confirmed violation.

### Info

An `info` flag identifies language that may warrant awareness or contextual review but is not necessarily discriminatory.

In this case, should record the flag and consider the surrounding context.

Example:

> "Family-friendly neighborhood."

Result:

```text
severity: info
can_publish: true
```

An informational flag should not automatically be treated as a Fair Housing violation.

## 5. Listing Review Process

Listings should follow this process before publication:

```text
Listing Description
        |
        v
ComplianceChecker
        |
        v
Identify Potential Issues
        |
   +----+----+----+
   |         |    |
 Error    Warning Info
   |         |    |
 Block    Review  Record
   |         |
   +----+----+
        |
        v
     Publish
```

### Error

The listing is blocked until the potentially prohibited language is addressed.

### Warning

The listing is sent for human review.

### Info

The listing may proceed, while the informational flag is recorded.

### No violations

The listing can proceed through the normal publication process.

## 6. Automated Checker Limitations

The ComplianceChecker uses predefined language patterns to identify potentially problematic phrases.

It may not identify every possible Fair Housing concern because:

* discriminatory meaning can depend on context;
* new or unexpected wording may not exist in the pattern library;
* the same phrase can have different meanings in different contexts;
* automated pattern matching cannot make a legal determination.

For these reasons, a clean result from the checker does not guarantee legal compliance.

Similarly, a flag does not necessarily mean that the listing is legally discriminatory.

Human review remains important for warnings, ambiguous cases, and changes to Fair Housing requirements.

## 7. Evaluation

The ComplianceChecker was evaluated using a test set containing known potentially prohibited descriptions and compliant descriptions.

Current evaluation results:

* True positives: 28
* False positives: 0
* False negatives: 0
* True negatives: 15
* Precision: 100%
* Recall: 100%
* Accuracy: 100%

The results demonstrate that the current implementation meets the project's target of 100% recall and greater than 80% precision on the test set.

## 8. Summary

The Fair Housing Compliance Checker provides an automated first layer of protection against potentially discriminatory listing language.

Its purpose is to:

* detect known problematic patterns;
* prevent obvious potentially prohibited language from being published;
* identify ambiguous language for human review; and
* provide a consistent compliance screening process.
