import mysql from "mysql2/promise";
declare const pool: mysql.Pool;
export declare function query<T>(sql: string, params?: any[]): Promise<T[]>;
export default pool;
