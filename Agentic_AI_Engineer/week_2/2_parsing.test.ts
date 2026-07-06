import { afterEach, beforeEach, describe, expect, it } from "../../../openclaw/node_modules/vitest";
import { parsePropertyQuery } from "./service.ts";

// week 2 - testing the parsePropertyQuery function
// Testing in terminal with following command: npm test -- src/skills/workshop/2_parsing.test.ts
describe("property query parsing (rets_property mapping)", () => {
  it("parses handbook example query correctly", async () => {
    const result = await parsePropertyQuery("3-bedroom condos in Irvine under $1.5M with a pool");
    expect(result).toMatchObject({
      L_City: "Irvine",
      L_SystemPrice: 1500000,
      L_Keyword2: 3,
      L_Type_: "Condominium",
      PoolPrivateYN: "True",
    });
  });

  it("parses query with city correctly", async () => {
    const result = await parsePropertyQuery("Show me homes in Newport Beach");
    expect(result).toMatchObject({
      L_City: "Newport Beach",
    });
  });

  it("parses bedroom count correctly", async () => {
    const result = await parsePropertyQuery("Show me 4-bedroom houses");
    expect(result).toMatchObject({
      L_Keyword2: 4,
    });
  });

  it("parses bathroom count correctly", async () => {
    const result = await parsePropertyQuery("Show me houses with 2 bathrooms");
    expect(result).toMatchObject({
      LM_Dec_3: 2,
    });
  });

  it("parses square footage correctly", async () => {
    const result = await parsePropertyQuery("Show me houses with 1500 sqft");
    expect(result).toMatchObject({
      LM_Int2_3: 1500,
    });
  });

  it("parses both bedroom and bathroom counts correctly", async () => {
    const result = await parsePropertyQuery("Show me a 4-bedroom house with 2 bathrooms");
    expect(result).toMatchObject({
      L_Keyword2: 4,
      LM_Dec_3: 2,
    });
  });

  it("parses price correctly", async () => {
    const result = await parsePropertyQuery("Show me houses under $500K");
    expect(result).toMatchObject({
      L_SystemPrice: 500000,
    });
  });

  it("parses property type correctly", async () => {
    const result = await parsePropertyQuery("Show me duplexes");
    expect(result).toMatchObject({
      L_Type_: "Duplex",
    });
  });

  it("parses pool and view correctly", async () => {
    const result = await parsePropertyQuery("Show me houses with a pool and no view");
    expect(result).toMatchObject({
      PoolPrivateYN: "True",
      ViewYN: null,
    });
  });

  it("parses association fees correctly", async () => {
    const result = await parsePropertyQuery("Show me houses with association fees under $500");
    expect(result).toMatchObject({
      AssociationFee: 500,
    });
  });

  it("parses complex queries correctly", async () => {
    const result = await parsePropertyQuery(
      "Show me 4-bedroom houses in Newport Beach under $600K with a pool and no view",
    );
    expect(result).toMatchObject({
      L_City: "Newport Beach",
      L_SystemPrice: 600000,
      L_Keyword2: 4,
      PoolPrivateYN: "True",
      ViewYN: null,
    });
  });

  it("parses city an price limit correctly", async () => {
    const result = await parsePropertyQuery("Show me houses in Los Angeles under $200K");
    expect(result).toMatchObject({
      L_City: "Los Angeles",
      L_SystemPrice: 200000,
    });
  });

  it("parses queries with townhouse property type correctly", async () => {
    const result = await parsePropertyQuery("Show me townhouses in Irvine under $1M");
    expect(result).toMatchObject({
      L_City: "Irvine",
      L_SystemPrice: 1000000,
      L_Type_: "Townhouse",
    });
  });
  it("parses queries with positive views correctly", async () => {
    const result = await parsePropertyQuery("Show me houses with a view");
    expect(result).toMatchObject({
      ViewYN: "True",
    });
  });
});
