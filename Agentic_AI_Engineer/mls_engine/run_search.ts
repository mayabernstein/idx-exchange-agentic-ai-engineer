import { run } from "./index";

declare const process: {
  argv: string[];
  exit(code?: number): never;
};

const query = process.argv.slice(2).join(" ");

run(query)
  .then(result => {
      console.log(JSON.stringify(result, null, 2));
  })
  .catch(err => {
      console.error(err);
      process.exit(1);
  });