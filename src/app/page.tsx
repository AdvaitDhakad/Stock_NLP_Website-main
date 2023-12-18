"use client";
import { createRoot } from "react-dom/client";
import { useRef, useState } from "react";
import React from "react";
import customParseFormat from "dayjs/plugin/customParseFormat";
import dayjs from "dayjs";
dayjs.extend(customParseFormat);
import type { DatePickerProps } from "antd";
import { Card, DatePicker, Space } from "antd";
import "react-datepicker/dist/react-datepicker.css";
import { data } from "autoprefixer";
import Image from "next/image";
import model2 from "/home/advait/Desktop/Stock_NLP_Website-main/public/model2.jpeg";

export default function Home() {
  const [article, setArticle] = useState("");
  const [resp, setResp] = useState("");
  const [sentiment, setSentiment] = useState("");
  const [loading, setLoading] = useState(false);
  const [date, setDate] = useState("");
  const [company, setCompany] = useState("");
  const [viewcompany, setviewcompany] = useState(false); //false
  const [viewmodel, setviewmodel] = useState(true); //false
  const [loading2, setLoading2] = useState(false); //false
  const [viewnews, setviewnews] = useState(false); //false
  const [resp2, setResp2] = useState("");
  const [resp3, setResp3] = useState("");
  const [viewtable, setviewtable] = useState(false); //false

  const handleSubmitDate = async (e: ReactFormEvent<HTMLFormElement>) => {
    // setLoading2(true)
    e.preventDefault();
    const resp3 = await fetch("http://localhost:5000/api/model/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ company: company }),
    });
    let resp4 = await resp3.json();
    setviewtable(true);
    setResp3(resp4);
    console.log(resp3);

    const resp2 = await fetch("http://localhost:5000/api/finance/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ company: company }),
    });
    let resp = await resp2.json();
    let news = resp.news_links;
    setviewnews(true);
    setResp2(news);
  };

  const handleSubmit = async (e: ReactFormEvent<HTMLFormElement>) => {
    setLoading(true);
    e.preventDefault();
    console.log(e.currentTarget.value);
    const res = await fetch("http://localhost:5000/api/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ sentence: article }),
    });
    // let res_j = await res
    let res_j = await res.json();
    let summ = res_j.summary;
    let sentiment = res_j.sentiment;

    // setResp(JSON.stringify(res_j))
    setResp(summ);
    setSentiment(sentiment);
    setLoading(false);
    setviewcompany(true);
  };
  return (
    <main className="flex min-h-screen flex-col">
      <div className="flex flex-col items-center justify-center">
        <h1 className="text-5xl font-bold text-center dark:text-neutral-50">
          Stock News Predictor
        </h1>
        <h4 className="text-2xl font-bold text-center dark:text-neutral-50">
          Next.js + Tailwind CSS + Flask + PyTorch+ BERT
        </h4>
      </div>
      <Card className="flex flex-col justify-center p-9 backdrop-blur-sm bg-white/10 m-9">
        <div className="grid-cols-1 grid-rows-1 sm:grid md:grid-cols-2">
          <div className="mx-3 mt-6 m-11 flex flex-col self-start border-blue-950 rounded-lg shadow-[0_2px_15px_-3px_rgba(0,0,0,0.07),0_10px_20px_-2px_rgba(0,0,0,004)]sm:shrink-0 sm:grow sm:basis-0 ">
            <div className="p-4 text-center rounded-md	border-2	">
              <h5 className="mb-2 text-xl rounded-md	font-medium leading-tight text-neutral-800 dark:text-neutral-50">
                ENTER YOUR NEWS
              </h5>
              <hr />
              <textarea
                name="news"
                className=" w-full pb-48 text-lg text-gray-900  bg-transparent dark:text-white"
                style={{ border: "none" }}
                placeholder="Your News Article..."
                value={article}
                onChange={(e) => setArticle(e.target.value)}
                required
              ></textarea>
            </div>
            <button
              onClick={handleSubmit}
              className="py-2.5  px-4 text-lg font-medium  text-center text-white rounded-lg focus:ring-4 focus:ring-blue-200 dark:focus:ring-blue-900 hover:bg-blue-800"
            >
              DONE
            </button>
          </div>
          <div
            className="mx-3 mt-6 flex flex-col self-start rounded-lg shadow-[0_2px_15px_-3px_rgba(0,0,0,0.07),0_10px_20px_-2px_rgba(0,0,0,0.
          04)] sm:shrink-0 sm:grow sm:basis-0"
          >
            <div className="p-4 pb-72 text-center rounded-md border">
              <h5 className="mb-2 text-xl font-medium leading-tight text-neutral-800 dark:text-neutral-50">
                SUMMARY
              </h5>
              <hr />
              {loading ? (
                <div
                  className="inline-block h-20 w-20 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] text-neutral-100 motion-reduce:animate-[spin_1.5s_linear_infinite]"
                  role="status"
                >
                  <span className="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]">
                    Loading...
                  </span>
                </div>
              ) : (
                <p
                  className={
                    " text-neutral-800 dark:text-neutral-50 text-lg rounded-md	" +
                    sentiment
                  }
                >
                  {resp}
                </p>
              )}
            </div>
          </div>
        </div>
        <div className="flex flex-col mx-8 border-2	rounded-md">
          {viewcompany ? (
            <div>
              <h5 className="mb-2 text-xl font-medium leading-tight text-center text-neutral-800 dark:text-neutral-50">
                COMPANY ANALYSIS
              </h5>
              <hr />
              <div className="mt-6">
                <div className="flex items-strech w-full ">
                  <div className="m-2 ml-10">
                    <h2 className="text-neutral-800 dark:text-neutral-50 text-lg">
                      Enter Company of which the news is about
                    </h2>
                    <input
                      type="text"
                      name="company"
                      className="w-48 pb-2 text-lg text-gray-900  bg-transparent dark:text-white border-none"
                      placeholder="Company Name..."
                      value={company}
                      onChange={(e) => setCompany(e.target.value)}
                      required
                    />{" "}
                    <br />
                  </div>
                  <div className="m-2 ml-10">
                    <h2 className="text-lg text-neutral-800 dark:text-neutral-50">
                      Enter the date of the news
                    </h2>
                    <DatePicker
                      className="bg-transparent font-light dark:text-white border-none text-lg w-48 pb-2"
                      defaultValue={dayjs("2023/01/01", "YYYY/MM/DD")}
                      format={"YYYY/MM/DD"}
                      selected={date}
                      maxDate={new Date()}
                      onChange={(date) => {
                        setDate(date);
                      }}
                      required
                    />
                  </div>
                  <div className="m-2 ml-72">
                    <h2 className="text-neutral-800 dark:text-neutral-50 text-lg">
                      LSTM BASED PREDICTIONS FOR STOCK PRICES
                    </h2>
                  </div>
                </div>
                <button
                  onClick={handleSubmitDate}
                  className=" flex flex-grow-0 py-2.5 m-10 mt-2 ml-44  px-4 w-64 justify-center text-lg font-medium  text-center text-white rounded-lg focus:ring-4 focus:ring-blue-200 dark:focus:ring-blue-900 hover:bg-blue-800"
                >
                  DONE
                </button>
              </div>
            </div>
          ) : null}
          {viewtable ? (
            <div className="flex flex-strech">
              <div className="text-lg text-neutral-800 dark:text-neutral-50">
                <h5 className="font-bold ml-64">Past 1 month Data</h5>
                <div
                  className="flex"
                  dangerouslySetInnerHTML={{ __html: resp3.data }}
                />
              </div>
              <div className="ml-32 h-full">
                <a
                  href="https://www.kaggle.com/code/advaitdhakad/stock-market-prediction-using-cnn-lstm-d6af07"
                  target="_blank"
                >
                  <Image
                    src={model2}
                    alt="model"
                    width={550}
                    height={1401}
                    className="rm-10"
                  />
                </a>
              </div>
            </div>
          ) : null}
        </div>

        <div className="flex flex-col mx-8 border-2 rounded-md mt-10	">
          {viewnews ? (
            <div className="">
              <h5 className="mb-2 text-xl font-medium leading-tight text-center text-neutral-800 dark:text-neutral-50">
                LINK TO COMPANY NEWS
              </h5>
              <hr />
              {/* <ul className='text-neutral-800 dark:text-neutral-50'><a href={resp2} /><p>Link</p></ul> */}
              {/* loop over resp2 and make each link clickable */}
              {Array.isArray(resp2) && (
                <ol className="text-neutral-800 dark:text-neutral-50">
                  {resp2.map((link, index) => (
                    <li key={index}>
                      <a
                        target="_blank"
                        className="flex flex-strech bg-blend-color-dodge"
                        href={link}
                      >
                        {index + 1}:{" "}
                        {link.length > 150 ? link.slice(0, 150) : link}....
                      </a>
                    </li>
                  ))}
                </ol>
              )}
              {/* <ul className="text-neutral-800 dark:text-neutral-50">
                  {resp2.map((link, index) => (
                    <a key={index} href={link}>
                      <p></p>
                    </a>
                  ))}
                </ul>
              )} */}
            </div>
          ) : null}
        </div>
      </Card>
    </main>
  );
}
