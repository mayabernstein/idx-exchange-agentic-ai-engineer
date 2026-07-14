// week 2 function
export async function parsePropertyQuery(query: string) {
  // Extract city
  const cityMatch = query.match(/in ([A-Za-z\s]+?)(?:\s+under|\s+with|\s+at|\s+for|$)/i);
  // Extract price
  const priceMatch = query.match(/under \$?([\d,.]+)(k|m)?/i);
  // Extract bedrooms
  const bedsMatch = query.match(/(\d+)[\s-]*(bed|beds|bedroom|bedrooms)/i);
  // Extract bathrooms
  const bathsMatch = query.match(/(\d+(?:\.5)?)[\s-]*(bath|baths|bathroom|bathrooms)/i);
  // Extract square footage
  const sqftMatch = query.match(/(\d+)[\s,]*(sqft|sq ft|square feet)/i);
  // Extract pool information
  const poolMatch = /pool/i.test(query);
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

  let maxPrice = null;
  if (priceMatch) {
    maxPrice = Number(priceMatch[1].replace(/,/g, ""));

    if (priceMatch[2]?.toLowerCase() === "k") maxPrice *= 1000;
    if (priceMatch[2]?.toLowerCase() === "m") maxPrice *= 1_000_000;
  }
  return {
    L_City: cityMatch?.[1]?.trim() || null,
    L_SystemPrice: maxPrice,
    L_Keyword2: bedsMatch ? Number(bedsMatch[1]) : null,
    LM_Dec_3: bathsMatch ? Number(bathsMatch[1]) : null,
    LM_Int2_3: sqftMatch ? Number(sqftMatch[1]) : null,
    L_Type_: typeKey ? typeMap[typeKey] : null,
    PoolPrivateYN: poolMatch ? 1 : null,
    ViewYN: viewMatch ? 1 : null,
    AssociationFee: maxHoa,
  };
}