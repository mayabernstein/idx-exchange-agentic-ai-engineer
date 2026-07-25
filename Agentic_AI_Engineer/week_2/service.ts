// week 2 function
export async function parsePropertyQuery(query: string) {
  console.log("USING SRC MLS ENGINE PARSER");
  // Extract city
  const cityMatch = query.match(/in ([A-Za-z\s]+?)(?:\s+under|\s+with|\s+at|\s+for|[.!?,]|$)/i);
  // Extract price
  const priceMatch = query.match(
  /(?:\$([\d,.]+)\s*(k|m|thousand|million)?|(?:budget|max(?:imum)?\s+price|price)\s+\$?([\d,.]+)\s*(k|m|thousand|million)?|(?:under|below)\s+\$([\d,.]+)\s*(k|m|thousand|million)?)/i
  );
  // Extract bedrooms
  const bedsMinMatch = query.match(
  /(?:at\s+least|minimum|min|more\s+than|over|greater\s+than)\s+(\d+)\s*(?:bed|beds|bedroom|bedrooms)/i
  );
  const bedsMaxMatch = query.match(
    /(?:up\s+to|maximum|max|less\s+than|under|fewer\s+than)\s+(\d+)\s*(?:bed|beds|bedroom|bedrooms)/i
  );
  const bedsExactMatch = query.match(
    /(\d+)\s*(?:bed|beds|bedroom|bedrooms)/i
  );
  // Extract bathrooms
  const bathsMinMatch = query.match(
  /(?:at\s+least|minimum|min|more\s+than|over|greater\s+than)\s+(\d+)\s*(?:bath|baths|bathroom|bathrooms)/i
  );
  const bathsMaxMatch = query.match(
    /(?:up\s+to|maximum|max|less\s+than|under|fewer\s+than)\s+(\d+)\s*(?:bath|baths|bathroom|bathrooms)/i
  );
  const bathsExactMatch = query.match(
    /(\d+)\s*(?:bath|baths|bathroom|bathrooms)/i
  );
  // Extract square footage
  const sqftMatch = query.match(/(\d+)[\s,]*(sqft|sq ft|square feet)/i);
  // Extract pool information
  const yesPoolMatch =
  /^(yes|yeah|yep|sure|correct)$|with\s+pool|want\s+(a\s+)?pool|pool/i.test(query);
  const noPoolMatch =
  /^(no|nope|nah)$|no\s+pool|without\s+pool|don't\s+want\s+(a\s+)?pool|do\s+not\s+want\s+(a\s+)?pool/i.test(query);
  // Extract view information
  const noViewMatch = /no view|without view/i.test(query);
  const viewMatch = /view/i.test(query) && !noViewMatch;
  // Extract association fees
  const hoaMatch = query.match(
    /(?:hoa|association fee|association fees)\s*(?:under|below|less than)?\s*\$?([\d,]+)/i,
  );

  let maxHoa = null;
  if (hoaMatch) {
    maxHoa = Number(hoaMatch[1].replace(/,/g, ""));
  }
  const typeMap: Record<string, string> = {
    condo: "Condominium",
    condominium: "Condominium",
    duplex: "Duplex",
    townhouse: "Townhouse",
    townhome: "Townhouse",
    "single family": "SingleFamilyResidence",
    "single-family": "SingleFamilyResidence",
    land: "UnimprovedLand",
  };
  const typeKey = Object.keys(typeMap).find((k) => query.toLowerCase().includes(k));
  const anyType = /\b(any|no preference|doesn't matter|does not matter|whatever|anything)\b/i.test(query);
  let maxPrice = null;

  if (priceMatch) {
      const value = priceMatch[1] ?? priceMatch[3] ?? priceMatch[5];
      const suffix = priceMatch[2] ?? priceMatch[4] ?? priceMatch[6];

      if (value) {
          maxPrice = Number(value.replace(/,/g, ""));

          if (
              suffix?.toLowerCase() === "k" ||
              suffix?.toLowerCase() === "thousand"
          ) {
              maxPrice *= 1000;
          }

          if (
              suffix?.toLowerCase() === "m" ||
              suffix?.toLowerCase() === "million"
          ) {
              maxPrice *= 1_000_000;
          }
      }
  }
  let minBeds = null;
  let maxBeds = null;
  let beds = null;
  if (bedsMinMatch) {
      minBeds = Number(bedsMinMatch[1]);
  }
  else if (bedsMaxMatch) {
      maxBeds = Number(bedsMaxMatch[1]);
  }
  else if (bedsExactMatch) {
      beds = Number(bedsExactMatch[1]);
  }
  let minBaths = null;
  let maxBaths = null;
  let baths = null;
  if (bathsMinMatch) {
      minBaths = Number(bathsMinMatch[1]);
  }
  else if (bathsMaxMatch) {
      maxBaths = Number(bathsMaxMatch[1]);
  }
  else if (bathsExactMatch) {
      baths = Number(bathsExactMatch[1]);
  }
  let poolValue = null;
  if (yesPoolMatch && !noPoolMatch) {
    poolValue = 1;
  }
  const poolAnswered = yesPoolMatch || noPoolMatch;
  return {
    L_City: cityMatch?.[1]?.trim() || null,
    L_SystemPrice: maxPrice,
    L_Keyword2: beds, 
    MinBeds: minBeds,
    MaxBeds: maxBeds,
    LM_Dec_3: baths,
    MinBaths: minBaths,
    MaxBaths: maxBaths, 
    LM_Int2_3: sqftMatch ? Number(sqftMatch[1]) : null,
    L_Type_: typeKey ? typeMap[typeKey] : null,
    AnyType: anyType,
    PoolPrivateYN: poolValue,
    PoolAnswered: poolAnswered, 
    ViewYN: viewMatch ? 1 : null,
    AssociationFee: maxHoa,
  };
}