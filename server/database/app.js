const cors = require("cors");
const express = require("express");
const fs = require("fs");
const path = require("path");
const mongoose = require("mongoose");

const Dealerships = require("./dealership");
const Reviews = require("./review");

const app = express();
const port = Number(process.env.PORT || 3030);
const mongoUrl = process.env.MONGO_URL || "mongodb://mongo_db:27017/dealershipsDB";

app.use(cors());
app.use(express.json({ limit: "1mb" }));
app.use(express.urlencoded({ extended: false }));

const readSeed = (filename, key) => {
  const filePath = path.join(__dirname, "data", filename);
  const payload = JSON.parse(fs.readFileSync(filePath, "utf8"));
  return payload[key] || [];
};

const seedDatabase = async () => {
  const dealerships = readSeed("dealerships.json", "dealerships");
  const reviews = readSeed("reviews.json", "reviews");
  await Promise.all([Dealerships.deleteMany({}), Reviews.deleteMany({})]);
  await Promise.all([Dealerships.insertMany(dealerships), Reviews.insertMany(reviews)]);
  console.log(`Seeded ${dealerships.length} dealerships and ${reviews.length} reviews.`);
};

app.get("/", (req, res) => res.send("Welcome to the Best Cars Mongoose API"));
app.get("/health", (req, res) => res.json({ status: "ok", database: mongoose.connection.readyState === 1 }));

app.get("/fetchReviews", async (req, res) => {
  try { res.json(await Reviews.find({}).sort({ id: 1 }).lean()); }
  catch (error) { console.error(error); res.status(500).json({ error: "Error fetching reviews" }); }
});

app.get("/fetchReviews/dealer/:id", async (req, res) => {
  try {
    const dealerId = Number(req.params.id);
    if (!Number.isInteger(dealerId)) return res.status(400).json({ error: "Dealer ID must be an integer" });
    res.json(await Reviews.find({ dealership: dealerId }).sort({ id: 1 }).lean());
  } catch (error) { console.error(error); res.status(500).json({ error: "Error fetching dealer reviews" }); }
});

app.get("/fetchDealers", async (req, res) => {
  try { res.json(await Dealerships.find({}).sort({ id: 1 }).lean()); }
  catch (error) { console.error(error); res.status(500).json({ error: "Error fetching dealerships" }); }
});

app.get("/fetchDealers/:state", async (req, res) => {
  try {
    const state = String(req.params.state || "").trim();
    if (!state || state.toLowerCase() === "all") return res.json(await Dealerships.find({}).sort({ id: 1 }).lean());
    const escaped = state.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const exactState = new RegExp(`^${escaped}$`, "i");
    res.json(await Dealerships.find({ $or: [{ state: exactState }, { st: exactState }] }).sort({ id: 1 }).lean());
  } catch (error) { console.error(error); res.status(500).json({ error: "Error filtering dealerships" }); }
});

app.get("/fetchDealer/:id", async (req, res) => {
  try {
    const dealerId = Number(req.params.id);
    if (!Number.isInteger(dealerId)) return res.status(400).json({ error: "Dealer ID must be an integer" });
    res.json(await Dealerships.find({ id: dealerId }).lean());
  } catch (error) { console.error(error); res.status(500).json({ error: "Error fetching dealership" }); }
});

app.post("/insert_review", async (req, res) => {
  try {
    const fields = ["name", "dealership", "review", "purchase", "purchase_date", "car_make", "car_model", "car_year"];
    const missing = fields.filter((field) => req.body[field] === undefined || req.body[field] === "");
    if (missing.length) return res.status(400).json({ error: `Missing fields: ${missing.join(", ")}` });
    const latest = await Reviews.findOne({}).sort({ id: -1 }).lean();
    const review = new Reviews({
      id: latest ? latest.id + 1 : 1,
      name: String(req.body.name), dealership: Number(req.body.dealership), review: String(req.body.review),
      purchase: Boolean(req.body.purchase), purchase_date: String(req.body.purchase_date),
      car_make: String(req.body.car_make), car_model: String(req.body.car_model), car_year: Number(req.body.car_year),
    });
    res.status(201).json(await review.save());
  } catch (error) { console.error(error); res.status(500).json({ error: "Error inserting review" }); }
});

const start = async () => {
  try {
    await mongoose.connect(mongoUrl);
    await seedDatabase();
    app.listen(port, "0.0.0.0", () => console.log(`Server is running on port ${port}`));
  } catch (error) { console.error("Unable to start database service:", error); process.exit(1); }
};
start();
